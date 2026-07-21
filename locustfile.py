from locust import HttpUser, task, between

class CarsUsers(HttpUser):
    wait_time = between(1, 2)

    @task
    def cars(self):
        self.client.get("/v1/cars/")


    @task
    def car_by_id(self):
        self.client.get("/v1/cars/225565558")


    @task
    def toyota(self):
        self.client.get("/v1/cars?brand=Toyota")