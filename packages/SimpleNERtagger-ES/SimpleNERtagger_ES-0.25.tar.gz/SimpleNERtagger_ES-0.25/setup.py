from distutils.core import setup
setup(
  name = 'SimpleNERtagger_ES',         # How you named your package folder (MyLib)
  packages = ['SimpleNERtagger_ES'],   # Chose the same as "name"
  version = '0.25',      # Start with a small number and increase it with every change you make
  license='',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This is an on-development NER-tagger in spanish. Regardless other NER-taggers in the market/wilds/Huggingface, this one will include non-common tags. Also, it will work with three kind of methods at the same time: deterministic and based on regular expressions (v0.1), transformer-based fine-tunned over preexisting data (v0.2) and LLM-prompt-based leveraging few-shot learning techniques (v0.3).',   # Give a short description about your library
  author = 'Jesús Armenta-Segura',                   # Type in your name
  author_email = 'jesus.jorge.armenta@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/JesusASmx/SimpleNERtagger_ES',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/JesusASmx/SimpleNERtagger_ES/archive/refs/tags/v024.tar.gz',
  keywords = ['NER', 'SPANISH', 'TAGGER'],   # Keywords that define your package best
  install_requires=['pandas', 'transformers'], # En esta versión 0.2 ya se incluyen màs requisitos.
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    'Programming Language :: Python :: 3.10',      #Specify which pyhton versions that you want to support
  ],
)
