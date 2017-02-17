# CCTV GIF Buffer

Poll IP CCTV cameras every a second, store the last 30 frames in memory per camera.

HTTP endpoint to retrieve a GIF of the past X seconds, plus future Y seconds. This service is designed to be easily integrated with home automation systems. Example uses:

* Send you a private message containing the last 20 seconds of motion when the door opens
* Post a GIF to a private slack channel when the door bell is rang

![Screenshot](https://raw.github.com/natm/cctv-gif-buffer/master/docs/demo1.gif)


## Deployment

### Quick and easy - Docker!

### Dependencies

libjpeg, install on Mac `brew install libjpeg`

### Installation

```
git@github.com:natm/cctv-gif-buffer.git
cd cctv-gif-buffer
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## License and Copyright

Copyright 2017 Nat Morris nat@nuqe.net

Licensed under the MIT License.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
