# Vonage Cloud Runtime SDK for Python

This is the Python SDK for [Vonage Cloud Runtime](https://developer.vonage.com/cloud-runtime). To use it you will need a Vonage account. Sign up for free at [vonage.com](https://dashboard.nexmo.com/sign-up?utm_source=DEV_REL&utm_medium=github&utm_campaign=vcr-sdk).

For full documentation refer to [developer.vonage.com](https://developer.vonage.com/vcr/overview).

## Installation

To install the SDK run:

```
pip install vonage_cloud_runtime
```

## Usage

The Vonage Cloud Runtime SDK gives you access to [providers](https://developer.vonage.com/vcr/providers/overview) which help you build powerful communication applications with Vonage. As an example here is how you can listen for incoming calls to your Vonage Application with the Voice provider:

```python
from vonage_cloud_runtime.vcr import VCR
from vonage_cloud_runtime.providers.voice.voice import Voice

vcr = VCR()
session = vcr.createSession()
voice = Voice(session)

await voice.onCall("onCall")

@app.post('/onCall')
async def onAnswer():
    return  [
                {
                    'action': 'talk',
                    'text': 'Hi from Vonage!'
                }
        ]
```

## Get Started

The Vonage Cloud Runtime SDK has been designed for use with the [Vonage Cloud Runtime Marketplace](https://developer.vonage.com/cloud-runtime). There you will find prebuilt solutions to common communication workflows with Vonage, where you can try them out and edit them to fit your use case. Once finished, you can deploy the application and let Vonage manage the hosting for you. 