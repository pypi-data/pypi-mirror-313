from setuptools import setup, find_packages

VERSION = '0.1.7'
DESCRIPTION = 'SHAP explainer with ChatGPT API'

# Setting up
setup(
    name="shap_explainer",
    version=VERSION,
    author="raytanghw (Ray Tang)",
    author_email="<raytanghw@gmail.com>",
    description=DESCRIPTION,
    packages=['shap_explainer'],
    install_requires=[
        'shap',
        'langchain'
    ],
    keywords=['python', 'shap', 'explainer', 'llm', 'chatgpt', 'xai'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
