from galtea.models.user import UserInput
from galtea.users.user_mail_notifier import UserEmailNotifier
from galtea.utils import generate_random_string, load_json, sanitize_string
import argilla as rg

class UserManager:
    def __init__(self, client: rg.Argilla):
        self._client = client
        self.user_mail_notifier = UserEmailNotifier()

    def generate_user_credentials(self, username: str, workspace: rg.Workspace, user: UserInput) -> dict:
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": username,
            "email": user.email,
            "password": generate_random_string(12),
            "role": user.role,
            "workspace": workspace
        }   
    
    def parse_username_from_email(self, email: str) -> str:
        return sanitize_string(email.split("@")[0])
    
    def _create_user(self, user_credentials: dict) -> list[rg.User, dict, bool]:
        
        user_already_exists = False

        _user = self._client.users(user_credentials['username'])

        if _user is not None:
            print(f"User {_user.username} already exists")
            user_already_exists = True
            return [_user, user_credentials, user_already_exists]
        
        user_to_create = rg.User(
            username=user_credentials['username'],
            password=user_credentials['password'],
            first_name=user_credentials['first_name'],
            last_name=user_credentials['last_name'],
            role=user_credentials['role'],
            client=self._client
        )
        
        _user = user_to_create.create()


        return [_user, user_credentials, user_already_exists]
    
    def _delete_user(self, user: rg.User):   

        print(f"Deleting user: {user.username}")     

        _user = self._client.users(user.username)

        if _user is not None:
            _user.delete()

        
    def create_users(self, workspace: rg.Workspace, users_path_file: str = "users.json"):
        users = load_json(users_path_file)

        for user in users:
            validated_input_user = UserInput.model_validate(user)
            username = self.parse_username_from_email(validated_input_user.email)
            new_user_credentials = self.generate_user_credentials(username, workspace, validated_input_user)

            created_user = self._create_user(new_user_credentials)
            
            if not created_user[2]:
                sent = self.user_mail_notifier.send_user_credentials(created_user[1])

                if not sent:
                    self._delete_user(created_user[0])
                    print(f"Error sending email to username: {created_user[0].username}, please check your email configuration or ensure that the email is valid") 
                    continue                    
                
            self._add_user_to_workspace(created_user[0].username, workspace)

    def _add_user_to_workspace(self, username: str, workspace: rg.Workspace):

        user = self._client.users(username)

        if user is None:
            raise ValueError(f"User {username} does not exist")


        if user in workspace.users:
            print(f"User {username} is already in workspace {workspace.name}")
            return
        

        try:
            user.add_to_workspace(workspace)
            print(f"User {username} added to workspace {workspace.name}")
            return

        except Exception as e:
            print(f"Error adding user {username} to workspace {workspace.name}: {e}")
            return
        