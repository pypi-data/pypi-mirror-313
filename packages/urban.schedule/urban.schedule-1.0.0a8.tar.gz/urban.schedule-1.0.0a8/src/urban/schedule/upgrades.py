# -*- coding: utf-8 -*-

from urban.schedule import utils

import logging

logger = logging.getLogger("urban.events: migrations")


def import_schedule_config(context):
    utils.import_all_config()


def update_reception(context):
    logger.info("starting : Update reception tasks")
    if "standard" in utils.get_configs():
        utils.import_all_config(
            base_json_path="./profiles/config/standard",
            handle_existing_content=utils.ExistingContent.UPDATE,
            match_filename="reception.json",
        )
    else:
        logger.info("nothing to upgrade")
    logger.info("upgrade done!")


def update_fd_opinion(context):
    logger.info("starting : Update fd opinion tasks")
    if "liege" in utils.get_configs():
        utils.import_all_config(
            base_json_path="./profiles/config/liege",
            handle_existing_content=utils.ExistingContent.UPDATE,
            match_filename="avis-fd.json",
        )
    else:
        logger.info("nothing to upgrade")
    logger.info("upgrade done!")


def update_reception_skip_existing(context):
    logger.info("starting : Update reception tasks (skip existing)")
    if "standard" in utils.get_configs():
        utils.import_all_config(
            base_json_path="./profiles/config/standard",
            handle_existing_content=utils.ExistingContent.SKIP,
            match_filename="reception.json",
         )
    else:
        logger.info("nothing to upgrade")
    logger.info("upgrade done!")

          
def import_roaddecree_schedule_config(context):
    logger.info("starting : Import roaddecree tasks")
    if "liege" in utils.get_configs():
        utils.import_all_config(
            base_json_path="./profiles/config/liege",
            handle_existing_content=utils.ExistingContent.UPDATE,
            match_filename="decision-notification.json",
        )
    else:
        utils.import_all_config(
            base_json_path="./profiles/standard/default",
            handle_existing_content=utils.ExistingContent.UPDATE,
            match_filename="decision-notification.json",
        )
    logger.info("upgrade done!")
