import json
import logging
import ssl
import time
import uuid
from threading import Thread

import websocket
from websocket import WebSocketConnectionClosedException

logger = logging.getLogger("PodiumLivestream")
logger.setLevel(logging.DEBUG)


class PodiumLivestream:
    PING_DELAY = 5.0
    WEBSOCKET_PING_INTERVAL = 10
    WEBSOCKET_PING_TIMEOUT = 5
    WEBSOCKET_RECONNECT_DELAY = 1.0

    def __init__(self):
        self.reply_uuid = str(uuid.uuid1().hex)
        self._running = False
        self._ws = None
        self._telemetry_stream_started_listener = None
        self._telemetry_stream_ended_listener = None
        self._list_telemetry_sessions_listener = None
        self._sensor_data_listener = None
        self._connection_open_listener = None
        self._connection_close_listener = None
        self._connection_warning_listener = None
        self._connection_error_listener = None
        self._alertmessage_listener = None
        self._alertmessage_ack_listener = None

    def set_telemetry_stream_started_listener(self, listener):
        self._telemetry_stream_started_listener = listener

    def set_telemetry_stream_ended_listener(self, listener):
        self._telemetry_stream_ended = listener

    def set_list_telemetry_sessions_listener(self, listener):
        self._list_telemetry_sessions_listener = listener

    def set_sensor_data_listener(self, listener):
        self._list_telemetry_sessions_listener = listener

    def set_connection_open_listener(self, listener):
        self._connection_open_listener = listener

    def set_connection_close_listener(self, listener):
        self._connection_close_listener = listener

    def set_connection_warning_listener(self, listener):
        self._connection_warning_listener = listener

    def set_connection_error_listener(self, listener):
        self._connection_error_listener = listener

    def set_alertmessage_listener(self, listener):
        self._alertmessage_listener = listener

    def set_alertmessage_ack_listener(self, listener):
        self._alertmessage_ack_listener = listener

    def on_telemetry_stream_started(self, body):
        eventdevice_id = body.get("eventDeviceId")
        device_id = body.get("deviceId")
        logger.info("PodiumLivestream: Telemetry stream started: {} {}".format(eventdevice_id, device_id))
        if listener := self._telemetry_stream_started_listener:
            listener(device_id, eventdevice_id)

    def on_telemetry_stream_ended(self, body):
        eventdevice_id = body.get("eventDeviceId")
        device_id = body.get("deviceId")
        logger.info("PodiumLivestream: telemetry stream ended: {} {}".format(eventdevice_id, device_id))
        if listener := self._telemetry_stream_ended_listener:
            listener(device_id, eventdevice_id)

    def on_list_telemetry_sessions(self, body):
        logger.debug("PodiumLivestream: ws_list_telemetry_sessions: {}".format(body))
        if listener := self._list_telemetry_sessions_listener:
            listener(body)

    def on_sensor_data(self, body):
        logger.debug("on sensordata %s", body)
        if listener := self._sensor_data_listener:
            listener(body)

    def on_ws_event(self, ws, body):
        logger.debug("on event: {}".format(body))

    def _on_ws_error(self, ws, error):
        logger.error("PodiumLivestream: Websocket error: {}".format(error))
        if listener := self._connection_error_listener:
            listener(error)

    def _on_ws_close(self, ws, close_status_code, close_msg):
        logger.info("PodiumLivestream: Websocket closed - status: %s - %s", close_status_code, close_msg)
        if listener := self._connection_close_listener:
            listener()

    def _on_connection_warning(self):
        logger.warning("Reconnecting: Your local internet is unstable")
        if listener := self._connection_warning_listener:
            listener()

    def _on_connection_open(self):
        logger.info("Connection opened")
        if listener := self._connection_open_listener:
            listener()

    def on_alertmessage(self, body):
        logger.info("on alertmessage %s", body)
        if listener := self._alertmessage_listener:
            listener(body)

    def on_alertmessageack(self, body):
        logger.info("on alertmessage ack %s", body)
        if listener := self._alertmessage_ack_listener:
            listener(body)

    def _websocket_send(self, msg):
        if not self._ws:
            logger.error("PodiumLivestream: could not send websocket message, websocket does not exist")
            return
        try:
            self._ws.send(msg)
        except WebSocketConnectionClosedException:
            logger.error("PodiumLivestream: Web socket is closed")
        except Exception as e:
            logger.error("PodiumLivestream: Failed to send websocket message {}".format(e))

    def unregister_sensor_data(self, eventdevice_id):
        logger.info("PodiumLivestream: unregistering sensor data for eventdevice_id {}".format(eventdevice_id))
        self._websocket_send('{{"type":"unregister","address":"event.{}"}}'.format(eventdevice_id))
        self._websocket_send('{{"type":"unregister","address":"sensorData.{}"}}'.format(eventdevice_id))
        self._websocket_send('{{"type":"unregister","address":"overviewData.{}"}}'.format(eventdevice_id))
        self._websocket_send('{{"type":"unregister","address":"alertmessage.{}"}}'.format(eventdevice_id))
        self._websocket_send('{{"type":"unregister","address":"alertmsgAck.{}"}}'.format(eventdevice_id))

    def register_sensor_data(self, eventdevice_id):
        logger.info("PodiumLivestream: registering sensor data for eventdevice_id {}".format(eventdevice_id))
        self._websocket_send('{{"type":"register","address":"event.{}"}}'.format(eventdevice_id))
        self._websocket_send('{{"type":"register","address":"sensorData.{}"}}'.format(eventdevice_id))
        self._websocket_send('{{"type":"register","address":"overviewData.{}"}}'.format(eventdevice_id))
        self._websocket_send('{{"type":"register","address":"alertmessage.{}"}}'.format(eventdevice_id))
        self._websocket_send('{{"type":"register","address":"alertmsgAck.{}"}}'.format(eventdevice_id))

    def list_telemetry_sessions(self):
        self._websocket_send(
            '{{"type":"send","address":"listTelemetryStreamSessions","body":{{}},"replyAddress":"{}"}}'.format(
                self.reply_uuid
            )
        )

    def open_connection(self, url, header):
        def ws_run_forever():

            # Enable this for viewing trace information
            # websocket.enableTrace(True)

            while True:  # TRY TO RECONNECT
                try:
                    self._ws = ws = websocket.WebSocketApp(
                        url,
                        on_open=self._on_ws_open,
                        on_message=self._on_ws_message,
                        on_error=self._on_ws_error,
                        on_close=self._on_ws_close,
                        header=header,
                    )
                    logger.info("PodiumLiveStream: Starting livestream")
                    ws.run_forever(
                        sslopt={"cert_reqs": ssl.CERT_NONE},
                        ping_interval=self.WEBSOCKET_PING_INTERVAL,
                        ping_timeout=self.WEBSOCKET_PING_TIMEOUT,
                    )

                    self._on_connection_warning()
                    logger.info("PodiumLiveStream: After livestream")
                    time.sleep(self.WEBSOCKET_RECONNECT_DELAY)
                except Exception as ex:
                    logger.warn("PodiumLiveStream: Exception after livestream connection: {}".format(ex))

        wst = Thread(target=ws_run_forever)
        wst.daemon = True
        wst.start()

    def close_connection(self):
        self._running = False
        self._ws.close()

    def dispatch_msg(self, ws, address, body):
        if address.startswith("sensorData"):
            self.on_sensor_data(body)
        elif address.startswith("event"):
            self.on_ws_event(body)
        elif address == "telemetryStreamStarted":
            self.on_telemetry_stream_started(body)
        elif address == "telemetryStreamEnded":
            self.on_telemetry_stream_ended(body)
        elif address == self.reply_uuid:
            self.on_list_telemetry_sessions(body)
        elif address.startswith("alertmessage"):
            self.on_alertmessage(body)
        elif address.startswith("alertmsgAck"):
            self.on_alertmessage_ack(body)

    def _on_ws_message(self, ws, message):
        logger.debug("PodiumLivestream: %s", message)
        msg = json.loads(message)
        address = msg.get("address")
        body = msg.get("body")
        if None not in [address, body]:
            self.dispatch_msg(ws, address, body)
        else:
            logger.error("PodiumLivestream: Malformed message received: {}".format(message))

    def _on_ws_open(self, ws):
        logger.info("PodiumLivestream: Websocket open")

        def run(*args):
            ws.send('{"type":"register","address":"telemetryStreamStarted"}')
            ws.send('{"type":"register","address":"telemetryStreamEnded"}')

            while self._running:
                try:
                    logger.debug("PodiumLivestream: websocket ping")
                    time.sleep(PodiumLivestream.PING_DELAY)
                    ws.send('{ "type": "ping" }')
                except WebSocketConnectionClosedException:
                    logger.error("PodiumLivestream: Websocket closed")
                    break
                except Exception as e:
                    logger.error("PodiumLivestream: failed to send ping: %s (%s)", e, type(e))

            logger.info("PodiumLivestream: Ping thread exiting")

        self._running = True
        t = Thread(target=run)
        t.daemon = True
        t.start()
        self._on_connection_open()
