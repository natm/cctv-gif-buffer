* Webserver thread
* Web app
    * Admin simple page
    * Endpoint to get events /event/UUID/
* Config class
* Redis interaction
* MQTT
    * publish once a minute: `cctvbuffer/status` : `{ version: 2.0.0, cameras: 9, uptime: 1234, count_snapshot: 0, count_animation: 0 }`
    * publish once a minute: `cctvbuffer/cameras` : `{ id1: name, id2: name }`
    * subscribe to: `cctvbuffer/snapshot/request/ch1/now`
    * publish to: `cctvbuffer/snapshot/event/ch1/info` : `{ id: ch1, name: name, bytes: 123, url: https://xxx/, timestamp: x, epoch: x, format: application/jpeg }`
    * publish to: `cctvbuffer/snapshot/event/ch1/data` : `RAWIMAGE`
    * subscribe to: `cctvbuffer/animation/request/ch1/now`
    * publish to: `cctvbuffer/animation/event/ch1/info` : `{ id: ch1, name: name, bytes: 123, url: https://xxx/, timestamp: x, epoch: x, duration: 10, format: application/gif  }`
    * publish to: `cctvbuffer/animation/event/ch1/data` : `RAWANIMATION`
* Timelapse
* Storage
    * Interface
    * Local
    * BackblazeB2
    * S3
* Test suite