"""
Command line interface to run the Anchor Connector
"""

import json
import os
from datetime import datetime, timedelta

from loguru import logger

from .connector import AnchorConnector


def load_env_var(var_name: str) -> str:
    """
    Load environment variable or throw error
    """
    var = os.environ.get(var_name)
    if var is None or var == "":
        raise ValueError(f"Environment variable {var_name} must be set.")
    return var


def main():  # pylint: disable=too-many-locals,too-many-statements
    """
    Main entrypoint to run the connector
    """
    base_url = load_env_var("ANCHOR_BASE_URL")
    base_graphql_url = load_env_var("ANCHOR_BASE_GRAPHQL_URL")
    webstation_id = load_env_var("ANCHOR_WEBSTATION_ID")
    anchorpw_s = load_env_var("ANCHOR_PW_S")

    connector = AnchorConnector(base_url, base_graphql_url, webstation_id, anchorpw_s)
    end = datetime.now()
    start = end - timedelta(days=30)

    episodes = connector.podcast_episode()
    logger.info("Podcast Episodes = {}", json.dumps(episodes, indent=4))

    impressions = connector.impressions()
    logger.info("Podcast Impressions = {}", json.dumps(impressions, indent=4))

    # Try a custom end date
    impressions = connector.impressions(
        datetime.now() - timedelta(days=30),
    )
    logger.info(
        "Podcast Impressions Custom Date = {}", json.dumps(impressions, indent=4)
    )

    plays = connector.plays(start, end)
    logger.info("Podcast Plays = {}", json.dumps(plays, indent=4))

    plays_by_age_range = connector.plays_by_age_range(start, end)
    logger.info(
        "Plays by Age Range = {}",
        json.dumps(plays_by_age_range, indent=4),
    )

    plays_by_app = connector.plays_by_app(start, end)
    logger.info(
        "Plays by App = {}",
        json.dumps(plays_by_app, indent=4),
    )

    plays_by_device = connector.plays_by_device(start, end)
    logger.info(
        "Plays by Device = {}",
        json.dumps(plays_by_device, indent=4),
    )

    plays_by_episode = connector.plays_by_episode(start, end)
    logger.info(
        "Plays by Episode = {}",
        json.dumps(plays_by_episode, indent=4),
    )

    plays_by_gender = connector.plays_by_gender(start, end)
    logger.info(
        "Plays by Gender = {}",
        json.dumps(plays_by_gender, indent=4),
    )

    plays_by_geo = connector.plays_by_geo()
    logger.info(
        "Plays by Geo = {}",
        json.dumps(plays_by_geo, indent=4),
    )

    # If the list of countries is not empty, get the first country in the list
    if len(plays_by_geo["data"]["rows"]) > 0:
        # Get the first entry in the list of plays by geo
        country = plays_by_geo["data"]["rows"][0][0]

        # Now use the geo to get the plays by geo on a city level
        plays_by_geo_city = connector.plays_by_geo_city(country)
        logger.info(
            "Plays by Geo City = {}",
            json.dumps(plays_by_geo_city, indent=4),
        )

    unique_listeners = connector.unique_listeners()
    logger.info("Podcast Unique Listeners = {}", json.dumps(unique_listeners, indent=4))

    audience_size = connector.audience_size()
    logger.info("Podcast Audience Size = {}", json.dumps(audience_size, indent=4))

    total_plays_by_episode = connector.total_plays_by_episode()
    logger.info(
        "Total Plays by Episode = {}",
        json.dumps(total_plays_by_episode, indent=4),
    )

    total_plays = connector.total_plays(True)
    logger.info("Podcast Total Plays = {}", json.dumps(total_plays, indent=4))

    for episode in connector.episodes():
        logger.info("Episode = {}", json.dumps(episode, indent=4))

        # depending on the api endpoint, we have to use different ids
        # (web_id=alphanumeric, episode_id=numeric)
        web_episode_id = episode["webEpisodeId"]

        episode_meta = connector.episode_plays(web_episode_id, start, end)
        logger.info("Episode Metadata = {}", json.dumps(episode_meta, indent=4))

        episode_performance = connector.episode_performance(web_episode_id)
        logger.info(
            "Episode Performance = {}", json.dumps(episode_performance, indent=4)
        )

        episode_aggregated_performance = connector.episode_aggregated_performance(
            web_episode_id
        )
        logger.info(
            "Episode Aggregated Performance = {}",
            json.dumps(episode_aggregated_performance, indent=4),
        )

        # pylint: disable=fixme
        # TODO: Fix video data. The API endpoint has changed with the migration to
        # 'Spotify for Creators'. The new endpoint is not yet implemented.
        # try:
        #     episode_all_time_video_data = connector.episode_all_time_video_data(
        #         episode_id
        #     )
        #     logger.info(
        #         "Episode All Time Video Data = {}",
        #         json.dumps(episode_all_time_video_data, indent=4),
        #     )
        # except requests.exceptions.HTTPError as e:  # pylint: disable=invalid-name
        #     if e.response.status_code == 404:
        #         # Handle the case when the episode has no video data or the URL
        #         # is incorrect
        #         logger.info("Episode has no video data or URL is incorrect")
        #     else:
        #         # Re-raise the exception if it's not a 404 error
        #         raise


if __name__ == "__main__":
    main()
