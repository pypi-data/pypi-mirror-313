#!/usr/bin/env python

import logging
import json


def post_payloads(msg_handler, payloads):
    """Processes the provided list payloads.

    The payloads are posted by the Message Handler.

    Parameters
    ----------
    msg_handler : __init__.py
        A message_handler object
    payloads : list
        The list of Slack App payloads to post

    Returns
    -------
    True
        If response from one or more of the POSTs have return code 200
    """

    # Proceed with the list of Slack App payloads if provided. The success counter is initially set to 0
    if isinstance(payloads, list):
        success_counter = 0
        for p in payloads:
            if isinstance(p, dict):
                p = json.dumps(p)
            msg_handler.set_payload(p)
            msg_handler.post_payload()

            # If any of the payloads are sent it is considered a success
            response_code = msg_handler.get_response_code()
            if isinstance(response_code, int) and response_code == 200:
                success_counter += 1
            else:
                logging.error(f"Failed to send message to Slack App. Response code {str(response_code)}.")

        # Return True if success so that we know at least one message have been sent
        if success_counter:
            logging.info(f"{success_counter} messages posted.")
            return True
