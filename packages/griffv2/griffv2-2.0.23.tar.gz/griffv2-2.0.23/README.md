# Griff V2

Librairie DDD

## Créer une nouvelle version de la librairie

Incrementer dans  `pyproject.toml` le n° de `version`.


## Publier Griff sur PyPi

Pour cela, il faut créer une nouvelle release sur GitHub avec le tag correspondant à la version de la librairie c'est à dire la version renseignée dans `pyproject.toml`.

- Aller sur la page GitHub du repository : https://github.com/Wedge-Digital/griff
- Cliquer sur `Tags`
- Cliquer sur `Releases`
- Cliquer sur `Draft a new release`
- Dans Choose a tag saisir la version de la raison = version renseignée dans `pyproject.toml`
- Cliquer sur `Generate release notes`
- Cliquer sur `Publish release`

Le CI s'occupera ensuite de publier la librairie sur PyPi si les tests ne sont pas KO.

## Importer les templates de code Griff

`File > Manage IDE Settings > Import Settings...` et sélectionner [live_template_settings.zip](live_template_settings.zip)
