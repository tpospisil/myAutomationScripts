import os, random
import datetime, names
from selenium import webdriver


def before_all(context):


def after_all(context):


def after_scenario(context, scenario):
    print("scenario status: " + str(scenario.status))
    if scenario.status == "failed":
        if not os.path.exists("failed_scenarios_screenshots"):
            os.makedirs("failed_scenarios_screenshots")
        os.chdir("failed_scenarios_screenshots")
        context.browser.save_screenshot(str(scenario.name) + "_failed.png")