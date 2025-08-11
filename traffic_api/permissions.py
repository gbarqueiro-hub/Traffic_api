from rest_framework.permissions import BasePermission, SAFE_METHODS

class CustomPermission(BasePermission):
    """
    Permissões:
    - Administrador (is_superuser): full access
    - Manager (grupo 'manager'): criar e ler, sem apagar
    - Anônimo (não autenticado): só leitura
    """

    def has_permission(self, request, view):
        user = request.user

        # Leitura liberada para todos
        if request.method in SAFE_METHODS:
            return True

        # Bloqueia escrita para anónimos
        if not user or not user.is_authenticated:
            return False

        # Admin pode tudo
        if user.is_superuser:
            return True

        # Manager pode criar/editar mas não apagar
        if user.groups.filter(name='manager').exists():
            return request.method != 'DELETE'

        # Qualquer outro autenticado sem permissões especiais não pode escrever
        return False