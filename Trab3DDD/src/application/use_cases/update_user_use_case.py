class UpdateUserUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, user_id, user_data):
        return self.user_repository.update(user_id, user_data)