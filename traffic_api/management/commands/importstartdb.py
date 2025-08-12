import os
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Importa o dump SQL completo do banco de dados'

    def handle(self, *args, **kwargs):
        caminho_dump = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..', 'data_storage', 'dump_completo.sql'
        )
        caminho_dump = os.path.normpath(caminho_dump)
        self.stdout.write(f'Usando dump SQL em: {caminho_dump}')

        # Configurações do banco - ajuste conforme seu ambiente!
        user = 'admin1'
        database = '1234'

        comando = [
            'psql',
            '-U', user,
            '-d', database,
            '-f', caminho_dump
        ]

        self.stdout.write('Importando dump SQL...')

        try:
            # Usa subprocess para melhor controle
            resultado = subprocess.run(comando, check=True, text=True, capture_output=True)
            self.stdout.write('Importação concluída com sucesso.')
        except subprocess.CalledProcessError as e:
            self.stderr.write('Erro durante a importação:')
            self.stderr.write(e.stderr)
