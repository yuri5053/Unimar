class CreateUserUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, user_data):
        user = self.user_repository.create(user_data)
        return user