[![Build Status](https://travis-ci.org/jaesivsm/the_conf.svg?branch=master)](https://travis-ci.org/jaesivsm/the_conf) [![Coverage Status](https://coveralls.io/repos/github/jaesivsm/the_conf/badge.svg?branch=master)](https://coveralls.io/github/jaesivsm/the_conf?branch=master)

From [this](http://sametmax.com/les-plus-grosses-roues-du-monde/)

    Une bonne lib de conf doit:

    * Offrir une API standardisée pour définir les paramètres qu’attend son programme sous la forme d’un schéma de données.
    * Permettre de générer depuis ce schéma les outils de parsing de la ligne de commande et des variables d’env.
    * Permettre de générer depuis ce schéma des validateurs pour ces schémas.
    * Permettre de générer des API pour modifier la conf.
    * Permettre de générer des UIs pour modifier la conf.
    * Séparer la notion de configuration du programme des paramètres utilisateurs.
    * Pouvoir marquer des settings en lecture seule, ou des permissions sur les settings.
    * Notifier le reste du code (ou des services) qu’une valeur à été modifiée. Dispatching, quand tu nous tiens…
    * Charger les settings depuis une source compatible (bdd, fichier, api, service, etc).
    * Permettre une hiérarchie de confs, avec une conf principale, des enfants, des enfants d’enfants, etc. et la récupération de la valeur qui cascade le long de cette hiérarchie. Un code doit pouvoir plugger sa conf dans une branche de l’arbre à la volée.
    * Fournir un service de settings pour les architectures distribuées.
    * Etre quand même utile et facile pour les tous petits scripts.
    * Auto documentation des settings.


Beforehand: for more clarity ```the_conf``` will designate the current program, its configuration will be referred to as the _meta conf_ and the configurations it will absorb (files / cmd line / environ) simply as the _configurations_.

# 1. read the _meta conf_

```the_conf``` should provide a singleton.
On instantiation the singleton would read the _meta conf_ (its configuration) from a file. YML and JSON will be considered first. This file will provide names, types, default values and if needed validator for options.

```the_conf``` will the validate the conf file. For each config value :
 * if value has _choices_ and _default value_, _default value_ has to be among _choices_.
 * if the value is nested, a node can't hold anything else than values
 * _required_ values can't have default

# 2. read the _configurations_

Once the _meta conf_ has been processed, ```the_conf``` will assemble all values at its reach from several sources.
Three types are to be considered:
 * files (again YML/JSON but maybe also later ini)
 * command line
 * environ
in this order of importance. This order must be itself overridable. ```the_conf``` must provide a backend for values from the configuration to be reached.

```python
the_conf.load('path/to/meta/conf.yml')
the_conf.nested.value
> 1
```

Upon reading _configurations_, ```the_conf``` will validate gathered values.
 * _configurations_ file type will be guessed from file extention (yaml / yml, json, ini), anything else must raise an error. Parsing errors won't also be silenced. Although, missing won't be an issue as long as all required values are gathered.
 * values must be in the type there declared in or cast to it without error
 * required values must be provided
 * if a value is configured with _choices_, the gathered value must be in _choices_

The first writable, readable available _configuration_ file found will be set as the main. Values will be edited on it but values from it will still be overridden according to the priorities. A warning should be issued if the main _configuration_ is overriddable.
If no suitable file is found, a warning should also be issued ; edition will be impossible and will generate an error.

# 3. generate the _configurations_

Provide an API to list and validate values needed from the _configurations_ (the required ones).
Provide a command line UI to process that list to let a user generate a _configuration_ file.

# 4. write the _configurations_

Depending on the permissions set in the _meta conf_, ```the_conf``` must allow to edit the values in the configuration file set as _main_ on read phase.
If editing a value which will be ignored for being overriden, a warning must be issued.
