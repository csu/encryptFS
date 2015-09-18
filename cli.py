import click

from encryptfs import EncryptFS

@click.command()
@click.argument('action', nargs=1)
@click.argument('password', nargs=1)
def main(action, password):
    encfs = EncryptFS(password)
    if action == 'encrypt':
        encfs.encrypt_all()
        click.echo("Encrypted all files.")
    elif action == 'decrypt':
        encfs.decrypt_all()
        click.echo("Dencrypted all files.")
    else:
        click.echo("Unknown action.")

if __name__ == '__main__':
    main()