ambition-slack
==============

Slack integration for Ambition

This project is hosted on Heroku and provides various integrations for Ambition's Slack service.

Configuring Slack Users
-----------------------
Add a SlackUser for every account in Ambition. The information for the account consists of the Slack username, the
email, and the full name of the person.

Github
------
A Github hook is provided in the Github app and exists at the url http://ambition-slack.herokuapp.com/github/.
This hook should be added as a webhook to every repo,
and it should be sent every event from the repo. The hook searches for messages about pull requests and about
comments on pull requests. If a user is tagged, they are notifed by their slack bot with the proper pull request URL.

To configure the Github integration, make a GithubUser model and point it to the proper SlackUser model. The GithubUser
model must contain the appropriate username on Github.
