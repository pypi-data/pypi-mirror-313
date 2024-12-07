import os
import time
import subprocess
from datetime import datetime
from tqdm import tqdm
from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage
import RPi.GPIO as GPIO
from gps import gps, WATCH_ENABLE, WATCH_NEWSTYLE


class GPSManager:
    def __init__(self, db_path='./gps_data.json', gpio_pin=20, timeout=300):
        """Initialize GPS Manager."""
        # Initialize GPIO
        self.gpio_pin = gpio_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)

        # Set working directory to script location
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(self.script_dir)

        # Initialize TinyDB with caching middleware
        self.db = TinyDB(db_path, storage=CachingMiddleware(JSONStorage))
        self.timeout = timeout

    def set_gpio_low(self):
        """Set GPIO pin to LOW."""
        GPIO.output(self.gpio_pin, GPIO.LOW)
        print("Starting GPS")

    def reset_gpio(self):
        """Reset GPIO pin (set it to HIGH)."""
        GPIO.output(self.gpio_pin, GPIO.HIGH)
        print("GPS Stopped")

    def start_gpsd(self):
        """Start the gpsd service."""
        try:
            subprocess.run(['sudo', 'systemctl', 'start', 'gpsd'], check=True)
            print("gpsd service started.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to start gpsd: {e}")

    def stop_gpsd(self):
        """Stop the gpsd service."""
        try:
            subprocess.run(['sudo', 'systemctl', 'stop', 'gpsd'], check=True)
            print("gpsd service stopped.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to stop gpsd: {e}")

    def get_gps_data(self):
        """Fetch GPS data using gpsd with a progress bar."""
        session = gps(mode=WATCH_ENABLE | WATCH_NEWSTYLE)
        print("Waiting for GPS fix...")

        with tqdm(total=self.timeout, desc="Time elapsed", unit="s") as pbar:
            start_time = time.time()
            while time.time() - start_time < self.timeout:
                elapsed = int(time.time() - start_time)
                pbar.n = elapsed
                pbar.last_print_n = elapsed  # Sync progress bar display
                pbar.refresh()

                try:
                    report = session.next()

                    # Display the current status on the same line
                    if report['class'] == 'SKY':
                        nSat = getattr(report, 'nSat', 0)
                        uSat = getattr(report, 'uSat', 0)
                        pbar.set_postfix_str(f"Satellites: {uSat}/{nSat} used")

                    if report['class'] == 'TPV' and getattr(report, 'mode', 0) >= 2:
                        # Successfully acquired fix
                        data = {
                            'latitude': getattr(report, 'lat', 'n/a'),
                            'longitude': getattr(report, 'lon', 'n/a'),
                            'altitude': getattr(report, 'alt', 'n/a'),
                            'time': getattr(report, 'time', 'n/a'),
                        }
                        pbar.set_postfix_str("GPS Fix Acquired!")
                        pbar.close()
                        print("\nGPS Data:", data)
                        return data

                except KeyError:
                    pbar.set_postfix_str("Waiting for valid data...")
                except StopIteration:
                    pbar.set_postfix_str("GPSD has terminated.")
                    break
                except Exception as e:
                    pbar.set_postfix_str(f"Error: {e}")

                time.sleep(1)

        pbar.close()
        print("\nTimeout reached: Unable to get GPS fix.")
        return None

    def save_gps_data(self, data):
        """Save GPS data to TinyDB with auto-increment ID and date_created."""
        try:
            # Get the last doc_id or start at 1
            metadata = self.db.search(Query().type == 'metadata')
            if metadata:
                last_id = metadata[0]['last_record_id']
            else:
                last_id = 0

            # Add auto-increment ID and date_created
            data['id'] = last_id + 1
            data['date_created'] = datetime.now().isoformat()

            # Save data to TinyDB
            doc_id = self.db.insert(data)

            # Update metadata with the new last_record_id
            self.db.upsert({'type': 'metadata', 'last_record_id': data['id']}, Query().type == 'metadata')

            # Flush cache to ensure data is saved
            self.db.storage.flush()

            print(f"GPS data saved with id: {data['id']} {data['latitude']}")
            return doc_id
        except Exception as e:
            print(f"Error saving GPS data: {e}")
            return None

    def get_last_gps_data(self):
        """Retrieve the last entered GPS data using the metadata last_record_id."""
        try:
            metadata = self.db.search(Query().type == 'metadata')
            if not metadata:
                print("No last_record_id metadata found.")
                return None

            last_record_id = metadata[0].get('last_record_id')
            if not last_record_id:
                print("last_record_id is missing.")
                return None

            # Retrieve the record with the highest ID
            last_record = self.db.get(Query().id == last_record_id)
            return last_record
        except Exception as e:
            print(f"Error retrieving GPS data: {e}")
            return None

    def run(self):
        """Main method to manage GPS process."""
        try:
            self.set_gpio_low()
            self.start_gpsd()
            gps_data = self.get_gps_data()

            if gps_data:
                self.save_gps_data(gps_data)
            else:
                print("No GPS data retrieved.")

            self.stop_gpsd()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.reset_gpio()
            GPIO.cleanup()
            print("Cleaned up")


