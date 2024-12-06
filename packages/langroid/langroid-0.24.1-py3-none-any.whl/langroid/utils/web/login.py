import requests
from bs4 import BeautifulSoup
from requests_oauthlib import OAuth2Session


def login_and_navigate(
    url: str,
    login: str,
    pw: str,
    page_link: str,
    client_id=None,
    client_secret=None,
    redirect_uri=None,
    scope=None,
    token_url=None,
    oauth_password=None,
):
    session = requests.Session()

    # Check if OAuth is needed
    if client_id and client_secret and redirect_uri and scope and token_url:
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
        authorization_url, state = oauth.authorization_url(url)
        session = oauth

        print(
            f"Please go to the following URL and authorize the app:"
            f" {authorization_url}"
        )
        authorization_response = input("Enter the full callback URL: ")

        # If an additional OAuth password is required
        if oauth_password:
            # Add the required password field to the token request
            token_params = {
                "password": oauth_password,
            }
        else:
            token_params = {}

        token = oauth.fetch_token(
            token_url,
            authorization_response=authorization_response,
            client_secret=client_secret,
            **token_params,
        )
        session.headers.update({"Authorization": f"Bearer {token['access_token']}"})

    response = session.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the login form and fill in the username and password fields
    login_form = soup.find("form")
    if not login_form:
        raise ValueError("Login form not found")

    form_data = {
        field.get("name"): field.get("value")
        for field in login_form.find_all("input")
        if field.get("name")
    }
    form_data[login] = login
    form_data[pw] = pw

    # Submit the login form
    login_url = url + login_form["action"]
    response = session.post(login_url, data=form_data)
    response.raise_for_status()

    # Navigate to the desired page
    response = session.get(page_link)
    response.raise_for_status()

    return response.text


# Example usage:
# response_text = login_and_navigate("https://example.com",
#                                    "your_username_field_name",
#                                    "your_password_field_name",
#                                    "https://example.com/target-page",
#                                    oauth_password="your_oauth_password")
# print(response_text)
