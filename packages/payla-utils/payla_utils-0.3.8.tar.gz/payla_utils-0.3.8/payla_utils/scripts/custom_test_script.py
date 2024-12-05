from django.contrib.auth import get_user_model


def run():
    test_user = get_user_model().objects.filter(username="test_user").first()
    if not test_user:
        test_user = get_user_model()(username="test_user")
        test_user.set_unusable_password()
        test_user.save()
