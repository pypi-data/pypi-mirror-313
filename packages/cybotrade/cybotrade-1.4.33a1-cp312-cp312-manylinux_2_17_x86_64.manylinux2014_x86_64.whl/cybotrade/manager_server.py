import asyncio
import logging
import json
import pkg_resources
from typing import Any

import aiohttp
import requests
from aiohttp import web
import os
import aiofiles
from cybotrade.models import OrderSide
from cybotrade.runtime import StrategyTrader

class ManagerServer():
    build_dir = './json-editor'

    def __init__(self, manager, logger: logging.Logger, strategy_trader):
        self.manager = manager 
        self.logger = logger
        self.strategy_trader = strategy_trader
        self.client = aiohttp.ClientSession()
        try:
            self.instance_id = os.environ["INSTANCE_ID"]
        except Exception as _:
            self.instance_id = '0'

    async def start(self, port):
        app = web.Application()
        async def on_shutdown(app):
            self.manager.on_shutdown()
        app.on_shutdown.append(on_shutdown)
        # app.router.add_static('/', path=self.build_dir, name='static')
        app.add_routes([web.post('/', self.on_signal())])
        app.add_routes([web.get('/update', self.serve_editor())])
        app.add_routes([web.post('/update', self.update_config())])
        app.add_routes([web.get('/get_config', self.get_config())])
        app.add_routes([web.post('/validate', self.validate())])
        logging.info("Starting ManagerServer")
        await web._run_app(app, port=port, access_log=self.logger)

    async def update_file(self, updated_config: Any):
        try:
            writable = json.dumps(updated_config)    
            file = await aiofiles.open("./config.json", mode="wt")
            await file.write(writable)
        except Exception as e:
            logging.error(f"Failed to update config.json with new json {updated_config}: {e}")

    def serve_editor(self):
        async def handler(_req: web.Request) -> web.FileResponse:
            return web.FileResponse(pkg_resources.resource_filename(__name__, '/static/index.html'))
        return handler

    def validate(self):
        async def handler(req: web.Request) -> web.StreamResponse:
            resp = web.Response()
            try:
                json_text = await req.text()
                body = json.loads(json_text)
                valid = False
                if self.instance_id != '0':
                    validate_resp = await self.client.get(
                        'https://api.cloud.cybotrade.rs/compute/instances',
                        headers={
                            "x-cybotrade-api-key": body["api_key"]
                        }
                    )
                    api_key_assc_instances = json.loads(await validate_resp.text())
                    for instance in api_key_assc_instances:
                        if instance["id"] == body["instance_id"]:
                            valid = True
                else:
                    valid = True
                if valid and body["instance_id"] == self.instance_id:
                    resp.set_status(200)
                    resp.text = "true"
                else:
                    resp.set_status(500)
                return resp;
            except Exception as e:
                resp.set_status(400)
                resp.text = str(e)
                return resp;
        return handler

    def get_config(self):
        # loop = asyncio.get_event_loop()
        # resp = web.Response()
        # resp.set_status(200)
        # resp.body = config
        async def handler(req: web.Request) -> web.StreamResponse:
            resp = web.Response()
            resp.set_status(200)
            resp.text = json.dumps((await self.strategy_trader.get_user_config()))
            return resp
        return handler
        # else:
        #     resp = web.Response()
        #     resp.set_status(400)
        #     return resp

    def update_config(self):
        async def handler(req: web.Request) -> web.StreamResponse:
            param_body = await req.text()
            try:
                body = json.loads(param_body)
                asyncio.create_task(self.update_file(body), name="config_update")
                resp = web.Response()
                resp.set_status(200)
                return resp
            except Exception as e:
                logging.error(f"Received invalid json: {param_body}: {e}");
                resp = web.Response()
                resp.set_status(400)
                return resp

        return handler

    def on_signal(self):
        async def handler(req: web.Request) -> web.StreamResponse:
            param_body = await req.text()
            try:
                body = json.loads(param_body)
                side = OrderSide.Sell
                if body["side"] == "buy":
                    side = OrderSide.Buy
                asyncio.create_task(self.manager.on_signal(id=body['id'], side=side, signal_params=body['signal_params']), name=f"signal_{id}")
                resp = web.Response()  
                resp.set_status(200)
                return resp
            except Exception as e:
                logging.error(f"Received invalid signal message: {param_body}: {e}");
                resp = web.Response()
                resp.set_status(400)
                return resp
                
        return handler
