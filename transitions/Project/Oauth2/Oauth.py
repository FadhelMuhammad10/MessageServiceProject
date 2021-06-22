from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView
from oauth2_provider.models import get_access_token_model

# get_access_token_model()
class AuthorizedTokensListView(LoginRequiredMixin, ListView):
    """
    Show a page where the current logged-in user can see his tokens so they can revoke them
    """
    context_object_name = "authorized_tokens"
    template_name = "oauth2_provider/authorized-tokens.html"
    model = get_access_token_model()

    def get_queryset(self):
        """
        Show only user"s tokens
        """
        print("enter authorize token list")
        return super().get_queryset().select_related("application").filter(
            user=self.request.user
        )


