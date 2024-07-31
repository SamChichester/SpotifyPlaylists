from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import os
from dotenv import load_dotenv


class SpotifyPlaylistsTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:3000')
        self.wait = WebDriverWait(self.driver, 10)
        load_dotenv()

    def tearDown(self):
        self.driver.quit()

    def test_home_page(self):
        driver = self.driver

        self.assertEqual(driver.title, 'Spotify Playlists Creator')

    def test_navigation_from_navbar(self):
        driver = self.driver
        wait = self.wait

        dropdown_button = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'button')))
        dropdown_button.click()

        artist_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Playlist From Artist')))
        artist_link.click()
        wait.until(EC.url_to_be('http://localhost:3000/playlist-from-artist'))
        self.assertEqual(driver.current_url, 'http://localhost:3000/playlist-from-artist')

        dropdown_button = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'button')))
        dropdown_button.click()

        genre_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Playlist From Genre")))
        genre_link.click()
        wait.until(EC.url_to_be('http://localhost:3000/playlist-from-genre'))
        self.assertEqual(driver.current_url, 'http://localhost:3000/playlist-from-genre')

        dropdown_button = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'button')))
        dropdown_button.click()

        top_tracks_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Playlist From Top Tracks")))
        top_tracks_link.click()
        wait.until(EC.url_to_be('http://localhost:3000/playlist-from-top-tracks'))
        self.assertEqual(driver.current_url, 'http://localhost:3000/playlist-from-top-tracks')

        dropdown_button = wait.until(EC.element_to_be_clickable((By.TAG_NAME, 'button')))
        dropdown_button.click()

        home_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Home")))
        home_link.click()
        wait.until(EC.url_to_be('http://localhost:3000/'))
        self.assertEqual(driver.current_url, 'http://localhost:3000/')

    def test_success_redirect(self):
        driver = self.driver
        wait = self.wait

        driver.get('http://localhost:3000/success')

        header = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        self.assertEqual(header.text, 'Welcome to Spotify Playlists Creator!')

    def test_create_playlist_from_artist_and_authentication(self):
        driver = self.driver
        wait = self.wait

        driver.find_element(By.LINK_TEXT, 'Create a playlist similar to a specific artist').click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Login with Spotify']")))

        if 'You need to log in to create a playlist' in driver.page_source:
            spotify_login_button = driver.find_element(By.XPATH, "//button[text()='Login with Spotify']")
            self.assertIsNotNone(spotify_login_button)
            spotify_login_button.click()

            wait.until(EC.presence_of_element_located((By.ID, 'login-username')))

            username_input = driver.find_element(By.ID, 'login-username')
            password_input = driver.find_element(By.ID, 'login-password')
            login_button = driver.find_element(By.ID, 'login-button')

            username_input.send_keys(os.environ.get('SPOTIFY_USERNAME'))
            password_input.send_keys(os.environ.get('SPOTIFY_PASSWORD'))
            login_button.click()

            wait.until(EC.url_contains('http://localhost:3000'))

        artist_input = self.wait.until(EC.presence_of_element_located((By.ID, 'artistName')))
        artist_input.send_keys('Coldplay')
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

        success_message = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[text()='Playlist Created Successfully!']")))
        self.assertIsNotNone(success_message)
        self.assertIn("Playlist Created Successfully!", driver.page_source)

    def test_create_playlist_from_genre(self):
        driver = self.driver
        wait = self.wait

        driver.get('http://localhost:3000/playlist-from-genre')
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Login with Spotify']")))

        if 'You need to log in to create a playlist' in driver.page_source:
            spotify_login_button = driver.find_element(By.XPATH, "//button[text()='Login with Spotify']")
            self.assertIsNotNone(spotify_login_button)
            spotify_login_button.click()

            wait.until(EC.presence_of_element_located((By.ID, 'login-username')))

            username_input = driver.find_element(By.ID, 'login-username')
            password_input = driver.find_element(By.ID, 'login-password')
            login_button = driver.find_element(By.ID, 'login-button')

            username_input.send_keys(os.environ.get('SPOTIFY_USERNAME'))
            password_input.send_keys(os.environ.get('SPOTIFY_PASSWORD'))
            login_button.click()

            wait.until(EC.url_contains('http://localhost:3000'))

        genres_dropdown = wait.until(EC.presence_of_element_located((By.ID, "genreSelect")))

        genres_dropdown.click()
        genres_dropdown.send_keys(Keys.DOWN)
        genres_dropdown.send_keys(Keys.RETURN)

        create_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        create_button.click()

        success_message = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/h1')))
        self.assertEqual(success_message.text, "Playlist Created Successfully!")

    def test_create_playlist_from_top_tracks_authenticated(self):
        driver = self.driver
        wait = self.wait

        driver.get("http://localhost:3000/playlist-from-top-tracks")
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='Login with Spotify']")))

        if 'You need to log in to create a playlist' in driver.page_source:
            spotify_login_button = driver.find_element(By.XPATH, "//button[text()='Login with Spotify']")
            self.assertIsNotNone(spotify_login_button)
            spotify_login_button.click()

            wait.until(EC.presence_of_element_located((By.ID, 'login-username')))

            username_input = driver.find_element(By.ID, 'login-username')
            password_input = driver.find_element(By.ID, 'login-password')
            login_button = driver.find_element(By.ID, 'login-button')

            username_input.send_keys(os.environ.get('SPOTIFY_USERNAME'))
            password_input.send_keys(os.environ.get('SPOTIFY_PASSWORD'))
            login_button.click()

            wait.until(EC.url_contains('http://localhost:3000'))

        timeframe_dropdown = wait.until(EC.presence_of_element_located((By.ID, "timeframeSelect")))

        timeframe_dropdown.click()
        timeframe_dropdown.send_keys(Keys.DOWN)
        timeframe_dropdown.send_keys(Keys.RETURN)

        create_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        create_button.click()

        success_message = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/h1')))
        self.assertEqual(success_message.text, "Playlist Created Successfully!")


if __name__ == "__main__":
    unittest.main()
