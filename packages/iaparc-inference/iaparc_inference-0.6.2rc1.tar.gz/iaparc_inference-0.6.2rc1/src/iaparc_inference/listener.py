"""
IA Parc Inference service
Support for inference of IA Parc models
"""
from json import dumps
from math import e
import os
import time
import asyncio
from re import T
import time
import uuid
from inspect import signature
import logging
import logging.config
import nats
from iaparc_inference.config import Config
from iaparc_inference.data_decoder import decode
from iaparc_inference.data_encoder import DataEncoder
from iaparc_inference.subscription import BatchSubscription

Error = ValueError | None

LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=LEVEL,
    force=True,
    format="%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
LOGGER = logging.getLogger("Inference")
LOGGER.propagate = True


class IAPListener():
    """
    Inference Listener class
    """

    def __init__(self,
                 callback,
                 decode=False,
                 batch:int=-1,
                 inputs:str = "",
                 outputs:str = "",
                 config_path:str= "/opt/pipeline/pipeline.json",
                 url:str="",
                 queue:str=""
                 ):
        """
        Constructor
        Arguments:
        - callback:     Callback function to proccess data
                        callback(data: Any | list[Any], parameters: Optional[dict])
        Optional arguments:
        - inputs:       Input queue name
        - outputs:      Output queue name
        - decode:       Set wether data should be decoded before calling the callback function (default: True)
        - batch:        Batch size for inference (default: -1)
                        If your model do not support batched input, set batch to 1
                        If set to -1, batch size will be determined by the BATCH_SIZE
                        environment variable
        - config_path:  Path to config file (default: /opt/pipeline/pipeline.json)
        - url:          Url of inference server (default: None)
                        By default determined by the NATS_URL environment variable,
                        however you can orverride it here
        - queue:        Name of queue (default: None)
                        By default determined by the NATS_QUEUE environment variable,
                        however you can orverride it here
        """
        # Init internal variables
        self.decode = decode
        self.timeout = 0.002
        self.exec_time = 0
        self._subs_in = []
        self._subs_out = []
        self._dag = Config(config_path)
        if inputs:
            self._dag.inputs = inputs
        self._links_in = self._dag.inputs.split(",")
        self._links_out = self._dag.outputs.split(",")

        self.lock = asyncio.Lock()
        self.callback = callback
        sig = signature(callback)
        self.callback_args = sig.parameters
        nb_params = len(self.callback_args)
        if nb_params == 1:
            self.callback_has_parameters = False
        else:
            self.callback_has_parameters = True

        if url:
            self.url = url
        else:
            self.url = os.environ.get("NATS_URL", "nats://localhost:4222")
        if queue:
            self.queue = queue.replace("/", "-")
        else:
            self.queue = os.environ.get(
                "NATS_QUEUE", "inference").replace("/", "-")
        if batch > 0:
            self.batch = batch
        else:
            self.batch = int(os.environ.get("BATCH_SIZE", 1))
        if self.batch > 1:
            self.is_batch = True
        else:
            self.is_batch = False

        self.error_queue = self.queue + ".ERROR"
        self.inputs = {}
        self.outputs = {}
        self.encoders = {}
        if len(self._dag.pipeline) == 0:
            print("No pipeline defined")
            quit(1)
        # Get inputs from first entity
        entity = self._dag.pipeline[0]
        for item in entity.input_def:
            if "link" in item and item["link"] in self._links_in:
                self.inputs[item["link"]] = item
        
        # Get outputs from last entity
        entity = self._dag.pipeline[-1]
        for item in entity.output_def:
            if "link" in item and item["link"] in self._links_out:
                if "name" in item:
                    item_name = item["name"]
                else:
                    item_name = item["link"]
                self.outputs[item_name] = item["link"]
                self.encoders[item["link"]] = DataEncoder(item)
        if outputs and outputs in self.outputs:
            self.default_output = self.outputs[outputs]
        else:
            self.default_output = self._links_out[0]

    @property
    def dag(self) -> Config:
        """ Input property """
        return self._dag

    @property
    def inputs_name(self) -> list:
        """ Input property """
        return self._links_in

    def run(self):
        """
        Run inference service
        """
        asyncio.run(self._run_async())

    async def _run_async(self):
        """ Start listening to NATS messages
        url: NATS server url
        batch_size: batch size
        """
        self.nc = await nats.connect(self.url)
        self.js = self.nc.jetstream()

        for q_name in self.inputs_name:
            #item = self.inputs[q_name]
            queue_in = self.queue + "." + q_name
            print("Listening on queue:", queue_in)
            js_in = await self.js.subscribe(queue_in+".>",
                                            queue=self.queue+"-"+q_name,
                                            stream=self.queue)
            self._subs_in.append((q_name, js_in))
            nc_in = await self.nc.subscribe("nc."+queue_in+".*.*", queue=self.queue+"-"+q_name)
            self._subs_in.append((q_name, nc_in))

        print("Default queue out:", self.default_output)
        self.data_store = await self.js.object_store(bucket=self.queue+"-data")

        os.system("touch /tmp/running")
        tasks = []
        for name, sub_in in self._subs_in:
            tasks.append(self.wait_msg(name, sub_in))
        await asyncio.gather(*tasks)
        await self.nc.close()

    async def wait_msg(self, name, sub_in):
        # Fetch and ack messagess from consumer.
        if sub_in.subject[:7] == "_INBOX.":
            subject = sub_in.subject[7:]
            is_js = True
        else:
            subject = sub_in.subject.replace(".*.*", "")
            is_js = False
        if self.is_batch:
            batch_sub = BatchSubscription(sub_in, self.batch)
        while True:
            if not self.is_batch:
                try:
                    msg = await sub_in.next_msg(timeout=600)
                except nats.errors.TimeoutError:
                    continue
                except TimeoutError:
                    continue
                except nats.errors.ConnectionClosedError:
                    LOGGER.error(
                        "Fatal error message handler: ConnectionClosedError")
                    break
                except asyncio.CancelledError:
                    LOGGER.error(
                        "Fatal error message handler: CancelledError")
                    break
                except Exception as e: # pylint: disable=W0703
                    LOGGER.error("Unknown error:", exc_info=True)
                    continue
                
                # Message received
                await asyncio.gather(
                    self.handle_msg(subject, name, [msg]),
                    self.term_msg([msg], is_js)
                )
            else:
                msgs = []
                ok = False
                try:
                    msgs = await batch_sub.get_batch(self.timeout)
                except nats.errors.TimeoutError:
                    continue
                except TimeoutError:
                    continue
                except nats.errors.ConnectionClosedError:
                    LOGGER.error(
                        "Fatal error message handler: ConnectionClosedError")
                    break
                except asyncio.CancelledError:
                    LOGGER.error(
                        "Fatal error message handler: CancelledError")
                    break
                
                # Messages received
                t0 = time.time()
                await asyncio.gather(
                    self.handle_msg(subject, name, msgs),
                    self.term_msg(msgs, is_js)
                )
                t1 = time.time()
                if self.exec_time == 0:
                    self.exec_time = t1 - t0
                self.exec_time = (self.exec_time + t1 - t0) / 2
                if self.exec_time < 0.02:
                    self.timeout = 0.002
                elif self.exec_time > 0.35:
                    self.timeout = 0.05
                else:
                    self.timeout = self.exec_time * 0.15

    async def handle_msg(self, subject, name, msgs):
        async with self.lock:
            if self.is_batch:
                uids, sources, batch, params_lst, content_types = zip(*[await self.get_data(subject, msg) for msg in msgs])
                batch = list(batch)
                await self._process_data(name, uids, sources, batch, content_types, params_lst)
            else:
                for msg in msgs:
                    uid, source, data, params, content_type = await self.get_data(subject, msg)
                    await self._process_data(name, [uid], [source], [data], [content_type], [params])

        return

    async def term_msg(self, msgs, is_js=False):
        if is_js:
            for msg in msgs:
                await msg.ack()
        else:
            ack = "".encode("utf8")
            for msg in msgs:
                await msg.respond(ack)

    async def get_data(self, subject, msg):
        l_sub = len(subject) + 1
        uid = msg.subject[(l_sub):]
        source = msg.headers.get("DataSource", "")
        params_lst = msg.headers.get("Parameters", "")
        params = {}
        if params_lst:
            for p in params_lst.split(","):
                args = p.split("=")
                if len(args) == 2:
                    k, v = args
                    params[k] = v
        content_type = msg.headers.get("ContentType", "")
        data = None
        if source == "object_store":
            obj_res = await self.data_store.get(msg.data.decode())
            data = obj_res.data
        else:
            data = msg.data

        return (uid, source, data, params, content_type)

    async def send_msg(self, out, uid, source, data, parameters={}, error=""):
        if error is None:
            error = ""
        _params = dumps(parameters)
        breply = "".encode()
        contentType = ""
        if out != self.error_queue:
            _out = self.queue + "." + out + "." + uid
            #print("Sending reply to:", _out)
            if data is not None:
                if source == "object_store":
                    store_uid = str(uuid.uuid4())
                    breply = store_uid.encode()
                    err = None
                    if isinstance(data, (bytes, bytearray)):
                        bdata = data
                    else:
                        bdata, contentType, err = self.encoders[out].encode(data)
                        if err:
                            _out = self.error_queue + "." + uid
                            breply = str(err).encode()
                            error = "Error encoding data"
                    if not err:
                        await self.data_store.put(store_uid, bdata)
                else :
                    if isinstance(data, (bytes, bytearray)):
                        breply = data
                    else:
                        breply, contentType, err = self.encoders[out].encode(data)
                        if err:
                            _out = self.error_queue + "." + uid
                            breply = str(err).encode()
                            error = "Error encoding data"
                    if len(breply) > 8388608: # 8MB
                        store_uid = str(uuid.uuid4())
                        source = "object_store"
                        bdata = breply
                        breply = store_uid.encode()
                        await self.data_store.put(store_uid, bdata)
        else:
            _out = self.error_queue + "." + uid
            breply = data.encode()
        
        headers = {"ProcessError": error,
                   "ContentType": contentType,
                   "DataSource": source,
                   "Parameters": _params}
        
        if out != self.error_queue:
            try:
                nc_out = "nc." + _out
                await self.nc.request(nc_out, breply, timeout=60, headers=headers)
                _sent = True
            except nats.errors.NoRespondersError:
                await self.js.publish(_out, breply, headers=headers)
            except Exception as e: # pylint: disable=W0703
                LOGGER.error("Error sending message on core NATS:", exc_info=True)
        else:
            await self.js.publish(_out, breply, headers=headers)

    async def _process_data(self, name: str,
                      uids: list,
                      sources: list,
                      raw_datas: list,
                      content_types: list,
                      reqs_parameters: list):
        """
        Process data
        Arguments:
        - requests:   list of data to process
        - is_batch:   is batched data
        """
        LOGGER.debug("handle request")
        queue_out = self.default_output
        p_datas = []
        p_sources = []
        p_uids = []
        p_params = []
        for uid, src, raw, ctype, params in zip(uids, sources, raw_datas, content_types, reqs_parameters):
            if self.decode:
                data, error = decode(raw, ctype, self.inputs[name])
                if error:
                    asyncio.create_task(self.send_msg(self.error_queue,
                                                      uid,
                                                      src,
                                                      str(error),
                                                      params,
                                                      "Wrong input"))
                    continue
                p_datas.append(data)
            else:
                p_datas.append(raw)
            p_sources.append(src)
            p_uids.append(uid)
            p_params.append(params)
        
        try_error = ""
        if len(p_datas) > 0:
            try:
                error = ""
                if self.is_batch:
                    if self.callback_has_parameters:
                        res = self.callback(p_datas, p_params)
                    else:
                        res = self.callback(p_datas)
                    if isinstance(res, tuple):
                        if len(res) == 2:
                            result, error = res
                        if len(res) == 3:
                            result, out, error = res
                            if out in self.outputs:
                                queue_out = self.outputs[out]
                    else:
                        result = res
                    if not isinstance(result, list):
                        error = "batch reply is not a list"
                    if len(p_datas) != len(result):
                        error = "batch reply has wrong size"
                    if error:
                        for uid, source, params in zip(p_uids, p_sources, p_params):
                            asyncio.create_task(self.send_msg(queue_out,
                                                              uid,
                                                              source,
                                                              error,
                                                              params,
                                                              error))
                    else:
                        for uid, source, res, params in zip(p_uids, p_sources, result, p_params):
                            asyncio.create_task(self.send_msg(queue_out,
                                                              uid,
                                                              source,
                                                              res,
                                                              params))
                else:
                    if len(p_params) > 0:
                        _params = p_params[0]
                    else:
                        _params = {}
                    if self.callback_has_parameters:
                        res = self.callback(p_datas[0], _params)
                    else:
                        res = self.callback(p_datas[0])
                    if isinstance(res, tuple):
                        if len(res) == 2:
                            result, error = res
                        if len(res) == 3:
                            result, out, error = res
                            if out in self.outputs:
                                queue_out = self.outputs[out]
                    else:
                        result = res
                    asyncio.create_task(self.send_msg(queue_out,
                                                      p_uids[0],
                                                      p_sources[0],
                                                      result,
                                                      _params,
                                                      error=error))
                
            except ValueError:
                LOGGER.error("Fatal error message handler", exc_info=True)
                try_error  = "Wrong input"
            except Exception as e: # pylint: disable=W0703
                LOGGER.error("Fatal error message handler", exc_info=True)
                try_error = f'Fatal error: {str(e)}'
            if try_error:
                for uid, source in zip(p_uids, p_sources):
                    asyncio.create_task(self.send_msg(
                        self.error_queue, uid, src, try_error, "Wrong input"))

