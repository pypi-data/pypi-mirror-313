'''
This file contains the endpoints for the Snapser API.
'''
from typing import Dict

END_POINTS: Dict[str, str] = {
    'DEV': 'https://gateway.dev.snapser.io/snapser',
    'DEV_TWO': 'https://gateway.dev.snapser.io/devtwo',
    'PLAYTEST': 'https://gateway.dev.snapser.io/playtest',
    'PROD': 'https://gateway.snapser.com/snapser'
}
