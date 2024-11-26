{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOwdTxPWb8vRY9EJknlMJ1R",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/stephanesq/Python_formation/blob/main/tap_spacex.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "**Assignment 4 -- custom tap**\n",
        "\n",
        "1. Utilise librairy singer\n",
        "2. Organise enregistreur de données (*Logger*) et schéma\n",
        "3. Récupérer les données"
      ],
      "metadata": {
        "id": "Cf3JVTOxJFdj"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "# librairies\n",
        "!pip install singer-python\n",
        "import singer\n",
        "import pandas as pd"
      ],
      "metadata": {
        "id": "4m2dJTJ5KJIi",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "22f2b1a2-3007-402e-8804-04a0ec764f29"
      },
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: singer-python in /usr/local/lib/python3.10/dist-packages (6.1.0)\n",
            "Requirement already satisfied: pytz>=2018.4 in /usr/local/lib/python3.10/dist-packages (from singer-python) (2024.2)\n",
            "Requirement already satisfied: jsonschema==2.*,>=2.6.0 in /usr/local/lib/python3.10/dist-packages (from singer-python) (2.6.0)\n",
            "Requirement already satisfied: simplejson==3.*,>=3.13.2 in /usr/local/lib/python3.10/dist-packages (from singer-python) (3.19.3)\n",
            "Requirement already satisfied: python-dateutil==2.*,>=2.7.3 in /usr/local/lib/python3.10/dist-packages (from singer-python) (2.8.2)\n",
            "Requirement already satisfied: backoff==2.*,>=2.2.1 in /usr/local/lib/python3.10/dist-packages (from singer-python) (2.2.1)\n",
            "Requirement already satisfied: ciso8601==2.*,>=2.3.1 in /usr/local/lib/python3.10/dist-packages (from singer-python) (2.3.1)\n",
            "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.10/dist-packages (from python-dateutil==2.*,>=2.7.3->singer-python) (1.16.0)\n"
          ]
        },
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "INFO NumExpr defaulting to 2 threads.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Logger\n",
        "LOGGER = singer.get_logger()\n",
        "\n",
        "schema = {\n",
        "    'properties': {\n",
        "        'id': {'type': 'string'},\n",
        "        'name': {'type': 'integer'},\n",
        "        'date_utc': {'type': 'string', 'format': 'date-time'}\n",
        "    }\n",
        "  }"
      ],
      "metadata": {
        "id": "Kika5HR_KUPK"
      },
      "execution_count": 2,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Fetch data avec la fonction main()\n",
        "def main():\n",
        "  url_api = 'https://api.spacexdata.com/v4/launches'\n",
        "  data_spacex = pd.read_json(url_api)\n",
        "\n",
        "  # Select and clean only the columns we want according to our schema\n",
        "  data_spacex_cleaned = data_spacex[['id', 'name', 'date_utc']].copy()\n",
        "\n",
        "  #transforme le dataframe en une liste de dictionnaires\n",
        "  #orient=records : chaque ligne devient un dictionnaire\n",
        "  records = data_spacex_cleaned.to_dict(orient='records')\n",
        "\n",
        "  singer.write_schema(stream_name='launches', schema=schema, key_properties=['id'])\n",
        "  singer.write_records(stream_name='launches', records=records)\n",
        "\n",
        "# fonction n'est exécuté que dans le script\n",
        "if __name__ == '__main__':\n",
        " #Appelle la fonction\n",
        "  main()"
      ],
      "metadata": {
        "id": "gCfiX3MdLOlj",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "cb815929-4ae4-4be5-d959-2923acbeb41c"
      },
      "execution_count": 7,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "{\"type\": \"SCHEMA\", \"stream\": \"launches\", \"schema\": {\"properties\": {\"id\": {\"type\": \"string\"}, \"name\": {\"type\": \"integer\"}, \"date_utc\": {\"type\": \"string\", \"format\": \"date-time\"}}}, \"key_properties\": [\"id\"]}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cd9ffd86e000604b32a\", \"name\": \"FalconSat\", \"date_utc\": \"2006-03-24T22:30:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cdaffd86e000604b32b\", \"name\": \"DemoSat\", \"date_utc\": \"2007-03-21T01:10:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cdbffd86e000604b32c\", \"name\": \"Trailblazer\", \"date_utc\": \"2008-08-03T03:34:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cdbffd86e000604b32d\", \"name\": \"RatSat\", \"date_utc\": \"2008-09-28T23:15:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cdcffd86e000604b32e\", \"name\": \"RazakSat\", \"date_utc\": \"2009-07-13T03:35:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cddffd86e000604b32f\", \"name\": \"Falcon 9 Test Flight\", \"date_utc\": \"2010-06-04T18:45:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cdeffd86e000604b330\", \"name\": \"COTS 1\", \"date_utc\": \"2010-12-08T15:43:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cdfffd86e000604b331\", \"name\": \"COTS 2\", \"date_utc\": \"2012-05-22T07:44:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87ce0ffd86e000604b332\", \"name\": \"CRS-1\", \"date_utc\": \"2012-10-08T00:35:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87ce1ffd86e000604b333\", \"name\": \"CRS-2\", \"date_utc\": \"2013-03-01T19:10:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87ce1ffd86e000604b334\", \"name\": \"CASSIOPE\", \"date_utc\": \"2013-09-29T16:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87ce2ffd86e000604b335\", \"name\": \"SES-8\", \"date_utc\": \"2013-12-03T22:41:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87ce3ffd86e000604b336\", \"name\": \"Thaicom 6\", \"date_utc\": \"2014-01-06T18:06:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87ce4ffd86e000604b337\", \"name\": \"CRS-3\", \"date_utc\": \"2014-04-18T19:25:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87ce4ffd86e000604b338\", \"name\": \"OG-2 Mission 1\", \"date_utc\": \"2014-07-14T15:15:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87ce5ffd86e000604b339\", \"name\": \"AsiaSat 8\", \"date_utc\": \"2014-08-05T08:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87ce6ffd86e000604b33a\", \"name\": \"AsiaSat 6\", \"date_utc\": \"2014-09-07T05:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87ce7ffd86e000604b33b\", \"name\": \"CRS-4\", \"date_utc\": \"2014-09-21T05:52:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87ce8ffd86e000604b33c\", \"name\": \"CRS-5\", \"date_utc\": \"2015-01-10T09:47:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87ceaffd86e000604b33d\", \"name\": \"DSCOVR\", \"date_utc\": \"2015-02-11T23:03:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87ceaffd86e000604b33e\", \"name\": \"ABS-3A / Eutelsat 115W B\", \"date_utc\": \"2015-03-02T03:50:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cecffd86e000604b33f\", \"name\": \"CRS-6\", \"date_utc\": \"2015-04-14T20:10:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cedffd86e000604b340\", \"name\": \"T\\u00fcrkmen\\u00c4lem 52\\u00b0E / MonacoSAT\", \"date_utc\": \"2015-04-27T23:03:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87ceeffd86e000604b341\", \"name\": \"CRS-7\", \"date_utc\": \"2015-06-28T14:21:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cefffd86e000604b342\", \"name\": \"OG-2 Mission 2\", \"date_utc\": \"2015-12-22T01:29:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cf0ffd86e000604b343\", \"name\": \"Jason 3\", \"date_utc\": \"2016-01-17T15:42:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cf2ffd86e000604b344\", \"name\": \"SES-9\", \"date_utc\": \"2016-03-04T23:35:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cf3ffd86e000604b345\", \"name\": \"CRS-8\", \"date_utc\": \"2016-04-08T20:43:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cf5ffd86e000604b346\", \"name\": \"JCSAT-2B\", \"date_utc\": \"2016-05-06T05:21:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cf6ffd86e000604b347\", \"name\": \"Thaicom 8\", \"date_utc\": \"2016-05-27T21:39:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cf8ffd86e000604b348\", \"name\": \"ABS-2A / Eutelsat 117W B\", \"date_utc\": \"2016-06-15T14:29:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cf9ffd86e000604b349\", \"name\": \"CRS-9\", \"date_utc\": \"2016-07-18T04:45:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cfaffd86e000604b34a\", \"name\": \"JCSAT-16\", \"date_utc\": \"2016-08-14T05:26:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cfbffd86e000604b34b\", \"name\": \"Amos-6\", \"date_utc\": \"2016-09-01T13:07:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cfdffd86e000604b34c\", \"name\": \"Iridium NEXT Mission 1\", \"date_utc\": \"2017-01-14T17:54:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cfeffd86e000604b34d\", \"name\": \"CRS-10\", \"date_utc\": \"2017-02-19T14:39:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87cfeffd86e000604b34e\", \"name\": \"EchoStar 23\", \"date_utc\": \"2017-03-16T06:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d00ffd86e000604b34f\", \"name\": \"SES-10\", \"date_utc\": \"2017-03-30T22:27:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d01ffd86e000604b350\", \"name\": \"NROL-76\", \"date_utc\": \"2017-05-01T11:15:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d01ffd86e000604b351\", \"name\": \"Inmarsat-5 F4\", \"date_utc\": \"2017-05-15T23:21:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d03ffd86e000604b352\", \"name\": \"CRS-11\", \"date_utc\": \"2017-06-03T21:07:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d04ffd86e000604b353\", \"name\": \"BulgariaSat-1\", \"date_utc\": \"2017-06-23T19:10:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d05ffd86e000604b354\", \"name\": \"Iridium NEXT Mission 2\", \"date_utc\": \"2017-06-25T20:25:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d06ffd86e000604b355\", \"name\": \"Intelsat 35e\", \"date_utc\": \"2017-07-05T23:35:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d07ffd86e000604b356\", \"name\": \"CRS-12\", \"date_utc\": \"2017-08-14T16:31:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d08ffd86e000604b357\", \"name\": \"FormoSat-5\", \"date_utc\": \"2017-08-24T18:50:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d09ffd86e000604b358\", \"name\": \"Boeing X-37B OTV-5\", \"date_utc\": \"2017-09-07T13:50:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d0affd86e000604b359\", \"name\": \"Iridium NEXT Mission 3\", \"date_utc\": \"2017-10-09T12:37:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d0cffd86e000604b35a\", \"name\": \"SES-11 / Echostar 105\", \"date_utc\": \"2017-10-11T22:53:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d0dffd86e000604b35b\", \"name\": \"KoreaSat 5A\", \"date_utc\": \"2017-10-30T19:34:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d0effd86e000604b35c\", \"name\": \"CRS-13\", \"date_utc\": \"2017-12-15T15:36:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d0fffd86e000604b35d\", \"name\": \"Iridium NEXT Mission 4\", \"date_utc\": \"2017-12-23T01:27:23.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d10ffd86e000604b35e\", \"name\": \"ZUMA\", \"date_utc\": \"2018-01-08T01:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d11ffd86e000604b35f\", \"name\": \"SES-16 / GovSat-1\", \"date_utc\": \"2018-01-31T21:25:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d13ffd86e000604b360\", \"name\": \"Falcon Heavy Test Flight\", \"date_utc\": \"2018-02-06T20:45:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d14ffd86e000604b361\", \"name\": \"Paz / Starlink Demo\", \"date_utc\": \"2018-02-22T14:17:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d15ffd86e000604b362\", \"name\": \"Hispasat 30W-6\", \"date_utc\": \"2018-03-06T05:33:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d16ffd86e000604b363\", \"name\": \"Iridium NEXT Mission 5\", \"date_utc\": \"2018-03-30T14:13:51.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d16ffd86e000604b364\", \"name\": \"CRS-14\", \"date_utc\": \"2018-04-02T20:30:41.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d18ffd86e000604b365\", \"name\": \"TESS\", \"date_utc\": \"2018-04-18T22:51:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d19ffd86e000604b366\", \"name\": \"Bangabandhu-1\", \"date_utc\": \"2018-05-11T20:14:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d1affd86e000604b367\", \"name\": \"Iridium NEXT Mission 6\", \"date_utc\": \"2018-05-22T19:47:58.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d1bffd86e000604b368\", \"name\": \"SES-12\", \"date_utc\": \"2018-06-04T04:45:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d1cffd86e000604b369\", \"name\": \"CRS-15\", \"date_utc\": \"2018-06-29T09:42:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d1effd86e000604b36a\", \"name\": \"Telstar 19V\", \"date_utc\": \"2018-07-22T05:50:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d1fffd86e000604b36b\", \"name\": \"Iridium NEXT Mission 7\", \"date_utc\": \"2018-07-25T11:39:26.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d20ffd86e000604b36c\", \"name\": \"Merah Putih\", \"date_utc\": \"2018-08-07T05:18:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d22ffd86e000604b36d\", \"name\": \"Telstar 18V\", \"date_utc\": \"2018-09-10T04:45:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d23ffd86e000604b36e\", \"name\": \"SAOCOM 1A\", \"date_utc\": \"2018-10-08T02:22:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d24ffd86e000604b36f\", \"name\": \"Es\\u2019hail 2\", \"date_utc\": \"2018-11-15T20:46:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d25ffd86e000604b370\", \"name\": \"SSO-A\", \"date_utc\": \"2018-12-03T18:34:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d26ffd86e000604b371\", \"name\": \"CRS-16\", \"date_utc\": \"2018-12-05T18:16:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d27ffd86e000604b372\", \"name\": \"GPS III SV01\", \"date_utc\": \"2018-12-23T13:51:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d28ffd86e000604b373\", \"name\": \"Iridium NEXT Mission 8\", \"date_utc\": \"2019-01-11T15:31:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d2affd86e000604b374\", \"name\": \"Nusantara Satu (PSN-6) / S5 / Beresheet\", \"date_utc\": \"2019-02-22T01:45:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d2bffd86e000604b375\", \"name\": \"CCtCap Demo Mission 1\", \"date_utc\": \"2019-03-02T07:45:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d2dffd86e000604b376\", \"name\": \"ArabSat 6A\", \"date_utc\": \"2019-04-11T22:35:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d2effd86e000604b377\", \"name\": \"CRS-17\", \"date_utc\": \"2019-05-04T06:48:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d30ffd86e000604b378\", \"name\": \"Starlink v0.9\", \"date_utc\": \"2019-05-24T02:30:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d31ffd86e000604b379\", \"name\": \"RADARSAT Constellation\", \"date_utc\": \"2019-06-12T14:17:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d35ffd86e000604b37a\", \"name\": \"STP-2\", \"date_utc\": \"2019-06-25T03:30:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d36ffd86e000604b37b\", \"name\": \"CRS-18\", \"date_utc\": \"2019-07-25T22:01:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d37ffd86e000604b37c\", \"name\": \"Amos-17\", \"date_utc\": \"2019-08-06T22:52:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d39ffd86e000604b37d\", \"name\": \"Starlink-1\", \"date_utc\": \"2019-11-11T14:56:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d39ffd86e000604b37e\", \"name\": \"CRS-19\", \"date_utc\": \"2019-12-05T17:29:23.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d3bffd86e000604b37f\", \"name\": \"JCSat 18 / Kacific 1\", \"date_utc\": \"2019-12-17T00:10:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d3cffd86e000604b380\", \"name\": \"Starlink-2\", \"date_utc\": \"2020-01-07T02:19:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d3dffd86e000604b381\", \"name\": \"Crew Dragon In Flight Abort Test\", \"date_utc\": \"2020-01-19T14:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d3fffd86e000604b382\", \"name\": \"Starlink-3\", \"date_utc\": \"2020-01-29T14:06:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d41ffd86e000604b383\", \"name\": \"Starlink-4\", \"date_utc\": \"2020-02-17T15:05:55.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d42ffd86e000604b384\", \"name\": \"CRS-20\", \"date_utc\": \"2020-03-07T04:50:31.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d43ffd86e000604b385\", \"name\": \"Starlink-5\", \"date_utc\": \"2020-03-18T12:16:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d44ffd86e000604b386\", \"name\": \"Starlink-6\", \"date_utc\": \"2020-04-22T19:30:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d46ffd86e000604b388\", \"name\": \"CCtCap Demo Mission 2\", \"date_utc\": \"2020-05-30T19:22:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d45ffd86e000604b387\", \"name\": \"Starlink-7\", \"date_utc\": \"2020-06-04T01:25:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d46ffd86e000604b389\", \"name\": \"Starlink-8 & SkySat 16-18\", \"date_utc\": \"2020-06-13T09:21:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d4affd86e000604b38b\", \"name\": \"GPS III SV03 (Columbus)\", \"date_utc\": \"2020-06-30T19:55:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d50ffd86e000604b394\", \"name\": \"ANASIS-II\", \"date_utc\": \"2020-07-20T21:30:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5ed9819a1f30554030d45c29\", \"name\": \"Starlink-9 (v1.0) & BlackSky Global 5-6\", \"date_utc\": \"2020-08-07T05:12:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5ed981d91f30554030d45c2a\", \"name\": \"Starlink-10 (v1.0) & SkySat 19-21\", \"date_utc\": \"2020-08-18T14:31:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d47ffd86e000604b38a\", \"name\": \"SAOCOM 1B, GNOMES-1, Tyvak-0172\", \"date_utc\": \"2020-08-30T23:18:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5ef6a1e90059c33cee4a828a\", \"name\": \"Starlink-11 (v1.0)\", \"date_utc\": \"2020-09-03T12:46:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5ef6a2090059c33cee4a828b\", \"name\": \"Starlink-12 (v1.0)\", \"date_utc\": \"2020-10-06T11:29:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5ef6a2bf0059c33cee4a828c\", \"name\": \"Starlink-13 (v1.0)\", \"date_utc\": \"2020-10-18T12:25:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5ef6a2e70059c33cee4a8293\", \"name\": \"Starlink-14 (v1.0)\", \"date_utc\": \"2020-10-24T15:31:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d4cffd86e000604b38d\", \"name\": \"GPS III SV04 (Sacagawea)\", \"date_utc\": \"2020-11-05T23:24:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d4dffd86e000604b38e\", \"name\": \"Crew-1\", \"date_utc\": \"2020-11-16T00:27:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5ed983aa1f30554030d45c31\", \"name\": \"Sentinel-6 Michael Freilich\", \"date_utc\": \"2020-11-21T17:17:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5fb95b3f3a88ae63c954603c\", \"name\": \"Starlink-15 (v1.0)\", \"date_utc\": \"2020-11-25T02:13:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d4effd86e000604b391\", \"name\": \"CRS-21\", \"date_utc\": \"2020-12-06T16:17:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d4bffd86e000604b38c\", \"name\": \"SXM-7\", \"date_utc\": \"2020-12-13T17:30:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5f8399fb818d8b59f5740d43\", \"name\": \"NROL-108\", \"date_utc\": \"2020-12-19T14:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d4fffd86e000604b393\", \"name\": \"Turksat 5A\", \"date_utc\": \"2021-01-08T02:15:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5fbfecce54ceb10a5664c80a\", \"name\": \"Starlink-16 (v1.0)\", \"date_utc\": \"2021-01-20T13:02:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5fd386aa7faea57d297c86c1\", \"name\": \"Transporter-1\", \"date_utc\": \"2021-01-24T15:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5ff6554f9257f579ee3a6c5f\", \"name\": \"Starlink-18 (v1.0)\", \"date_utc\": \"2021-02-04T06:19:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"600f9a5e8f798e2a4d5f979c\", \"name\": \"Starlink-19 (v1.0)\", \"date_utc\": \"2021-02-16T03:59:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5fbfecfe54ceb10a5664c80b\", \"name\": \"Starlink-17 (v1.0)\", \"date_utc\": \"2021-03-04T08:24:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"600f9a718f798e2a4d5f979d\", \"name\": \"Starlink-20 (v1.0)\", \"date_utc\": \"2021-03-11T08:13:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"600f9a8d8f798e2a4d5f979e\", \"name\": \"Starlink-21 (v1.0)\", \"date_utc\": \"2021-03-14T10:01:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"60428aafc041c16716f73cd7\", \"name\": \"Starlink-22 (v1.0)\", \"date_utc\": \"2021-03-24T08:28:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"60428ac4c041c16716f73cd8\", \"name\": \"Starlink-23 (v1.0)\", \"date_utc\": \"2021-04-07T16:34:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5fe3af58b3467846b324215f\", \"name\": \"Crew-2\", \"date_utc\": \"2021-04-23T09:49:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"605b4b6aaa5433645e37d03f\", \"name\": \"Starlink-24 (v1.0)\", \"date_utc\": \"2021-04-29T03:44:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"605b4b7daa5433645e37d040\", \"name\": \"Starlink-25 (v1.0)\", \"date_utc\": \"2021-05-04T19:01:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6079bd1c9a06446e8c61bf76\", \"name\": \"Starlink-27 (v1.0)\", \"date_utc\": \"2021-05-09T06:42:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"605b4b95aa5433645e37d041\", \"name\": \"Starlink-26 (v1.0) + Capella-6 + Tyvak-0130\", \"date_utc\": \"2021-05-15T22:54:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6079bd399a06446e8c61bf77\", \"name\": \"Starlink-28 (v1.0)\", \"date_utc\": \"2021-05-26T18:59:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5fe3af84b3467846b3242161\", \"name\": \"CRS-22 & IROSA\", \"date_utc\": \"2021-06-03T17:29:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5fe3af6db3467846b3242160\", \"name\": \"SXM-8\", \"date_utc\": \"2021-06-06T04:26:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5eb87d4effd86e000604b390\", \"name\": \"GPS III SV05\", \"date_utc\": \"2021-06-17T16:09:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"600f9b6d8f798e2a4d5f979f\", \"name\": \"Transporter-2\", \"date_utc\": \"2021-06-30T19:31:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5fe3b11eb3467846b324216c\", \"name\": \"CRS-23\", \"date_utc\": \"2021-08-29T07:14:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"60e3bf0d73359e1e20335c37\", \"name\": \"Starlink 2-1 (v1.5)\", \"date_utc\": \"2021-09-14T03:55:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"607a37565a906a44023e0866\", \"name\": \"Inspiration4\", \"date_utc\": \"2021-09-16T00:02:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5fe3b15eb3467846b324216d\", \"name\": \"Crew-3\", \"date_utc\": \"2021-11-11T02:03:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"618faad2563d69573ed8ca9d\", \"name\": \"Starlink 4-1 (v1.5)\", \"date_utc\": \"2021-11-13T12:40:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5fe3b107b3467846b324216b\", \"name\": \"DART\", \"date_utc\": \"2021-11-24T06:20:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6161c94c6db1a92bfba85349\", \"name\": \"Starlink 4-3 (v1.5)\", \"date_utc\": \"2021-12-01T23:20:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6161c88d6db1a92bfba85348\", \"name\": \"IXPE\", \"date_utc\": \"2021-12-09T06:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"61bba806437241381bf7061e\", \"name\": \"Starlink 4-4 (v1.5)\", \"date_utc\": \"2021-12-18T12:41:40.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5fe3afc1b3467846b3242164\", \"name\": \"T\\u00fcrksat 5B\", \"date_utc\": \"2021-12-19T03:58:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6161d2006db1a92bfba85356\", \"name\": \"CRS-24\", \"date_utc\": \"2021-12-21T10:06:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"61d5eca1f88e4c5fc91f1eb7\", \"name\": \"Starlink 4-5 (v1.5)\", \"date_utc\": \"2022-01-06T21:49:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"61bf3e31cd5ab50b0d936345\", \"name\": \"Transporter-3\", \"date_utc\": \"2022-01-13T15:25:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"61e048bbbe8d8b66799018d0\", \"name\": \"Starlink 4-6 (v1.5)\", \"date_utc\": \"2022-01-19T00:04:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6161d32d6db1a92bfba85359\", \"name\": \"CSG-2\", \"date_utc\": \"2022-01-31T23:11:12.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"607a34e35a906a44023e085e\", \"name\": \"NROL-87\", \"date_utc\": \"2022-02-02T20:18:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"61e048ffbe8d8b66799018d1\", \"name\": \"Starlink 4-7 (v1.5)\", \"date_utc\": \"2022-02-03T18:13:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"61fc01dae0dc5662b76489a7\", \"name\": \"Starlink 4-8 (v1.5)\", \"date_utc\": \"2022-02-21T14:44:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"61fc0203e0dc5662b76489a8\", \"name\": \"Starlink 4-11 (v1.5)\", \"date_utc\": \"2022-02-25T17:12:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"61fc0224e0dc5662b76489ab\", \"name\": \"Starlink 4-9 (v1.5)\", \"date_utc\": \"2022-03-03T14:35:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"61fc0243e0dc5662b76489ae\", \"name\": \"Starlink 4-10 (v1.5)\", \"date_utc\": \"2022-03-09T13:45:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6234908cf051102e1fcedac4\", \"name\": \"Starlink 4-12 (v1.5)\", \"date_utc\": \"2022-03-19T03:24:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6243ad8baf52800c6e919252\", \"name\": \"Transporter-4\", \"date_utc\": \"2022-04-01T16:24:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"61eefaa89eb1064137a1bd73\", \"name\": \"Ax-1\", \"date_utc\": \"2022-04-08T15:17:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6243adcaaf52800c6e919254\", \"name\": \"NROL-85\", \"date_utc\": \"2022-04-17T13:13:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6243ada6af52800c6e919253\", \"name\": \"Starlink 4-14 (v1.5)\", \"date_utc\": \"2022-04-21T15:16:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6243ade2af52800c6e919255\", \"name\": \"Crew-4\", \"date_utc\": \"2022-04-27T07:52:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62582a6f5988f159024b964b\", \"name\": \"Starlink 4-16 (v1.5)\", \"date_utc\": \"2022-04-29T21:27:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62582a855988f159024b964c\", \"name\": \"Starlink 4-17 (v1.5)\", \"date_utc\": \"2022-05-06T09:42:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6258290d5988f159024b9644\", \"name\": \"Starlink 4-13 (v1.5)\", \"date_utc\": \"2022-05-13T22:07:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"625828f25988f159024b9643\", \"name\": \"Starlink 4-15 (v1.5)\", \"date_utc\": \"2022-05-14T20:40:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62615ebc0ec008379be596fa\", \"name\": \"Starlink 4-18 (v1.5)\", \"date_utc\": \"2022-05-18T10:40:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6243ae24af52800c6e919258\", \"name\": \"Transporter-5\", \"date_utc\": \"2022-05-25T18:27:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6243ae0aaf52800c6e919257\", \"name\": \"Nilesat-301\", \"date_utc\": \"2022-06-08T21:04:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6278481757b51b752c5c5a5f\", \"name\": \"Starlink 4-19 (v1.5)\", \"date_utc\": \"2022-06-01T17:08:50.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"5fe3af43b3467846b324215e\", \"name\": \"SARah 1\", \"date_utc\": \"2022-06-18T14:19:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62a9f08b20413d2695d88711\", \"name\": \"Globalstar FM15\", \"date_utc\": \"2022-06-19T04:27:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6243aea5af52800c6e91925c\", \"name\": \"SES-22\", \"date_utc\": \"2022-06-29T21:04:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62a9f0c920413d2695d88712\", \"name\": \"Starlink 4-21 (v1.5)\", \"date_utc\": \"2022-07-07T13:11:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62a9f0e320413d2695d88713\", \"name\": \"Starlink 3-1 (v1.5)\", \"date_utc\": \"2022-07-11T01:39:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6243ae40af52800c6e919259\", \"name\": \"CRS-25\", \"date_utc\": \"2022-07-15T00:44:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62a9f0f820413d2695d88714\", \"name\": \"Starlink 4-22 (v1.5)\", \"date_utc\": \"2022-07-17T14:50:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62a9f10b20413d2695d88715\", \"name\": \"Starlink 3-2 (v1.5)\", \"date_utc\": \"2022-07-21T17:13:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62a9f12820413d2695d88716\", \"name\": \"Starlink 4-25 (v1.5)\", \"date_utc\": \"2022-07-24T00:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62a9f86420413d2695d88719\", \"name\": \"KPLO\", \"date_utc\": \"2022-08-04T23:08:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62a9f8b320413d2695d8871b\", \"name\": \"Starlink 4-26 (v1.5)\", \"date_utc\": \"2022-08-09T22:57:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62f3b4ff0f55c50e192a4e6b\", \"name\": \"Starlink 3-3 (v1.5)\", \"date_utc\": \"2022-08-12T21:30:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62f3b5200f55c50e192a4e6c\", \"name\": \"Starlink 4-27 (v1.5)\", \"date_utc\": \"2022-08-19T19:24:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62f3b5290f55c50e192a4e6d\", \"name\": \"Starlink 4-23 (v1.5)\", \"date_utc\": \"2022-08-28T02:22:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62f3b53a0f55c50e192a4e6f\", \"name\": \"Starlink 3-4 (v1.5)\", \"date_utc\": \"2022-08-31T05:40:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62f3b5330f55c50e192a4e6e\", \"name\": \"Starlink 4-20 (v1.5) & Sherpa LTC-2/Varuna-TDM\", \"date_utc\": \"2022-09-05T02:09:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62a9f89a20413d2695d8871a\", \"name\": \"Starlink 4-2 (v1.5) & Blue Walker 3\", \"date_utc\": \"2022-09-11T01:10:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"63161329ffc78f3b8567070b\", \"name\": \"Starlink 4-34 (v1.5)\", \"date_utc\": \"2022-09-17T01:05:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"63161339ffc78f3b8567070c\", \"name\": \"Starlink 4-35 (v1.5)\", \"date_utc\": \"2022-09-24T23:30:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"62dd70d5202306255024d139\", \"name\": \"Crew-5\", \"date_utc\": \"2022-10-05T16:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6243aec2af52800c6e91925d\", \"name\": \"USSF-44\", \"date_utc\": \"2022-11-01T13:41:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"63161345ffc78f3b8567070d\", \"name\": \"Starlink 4-36 (v1.5)\", \"date_utc\": \"2022-10-20T14:50:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"633f71240531f07b4fdf59bb\", \"name\": \"Galaxy 33 (15R) & 34 (12R)\", \"date_utc\": \"2022-10-08T23:05:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"633f71370531f07b4fdf59bc\", \"name\": \"Hotbird 13F\", \"date_utc\": \"2022-10-15T05:22:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"633f71dd0531f07b4fdf59c1\", \"name\": \"Hotbird 13G\", \"date_utc\": \"2022-11-03T03:24:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"633f71a90531f07b4fdf59be\", \"name\": \"Galaxy 31 (23R) & 32 (17R)\", \"date_utc\": \"2022-11-08T00:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"633f71b60531f07b4fdf59bf\", \"name\": \"Eutelsat 10B\", \"date_utc\": \"2022-11-15T00:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"633f723d0531f07b4fdf59c4\", \"name\": \"ispace Mission 1 & Rashid\", \"date_utc\": \"2022-11-22T00:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"633f71cc0531f07b4fdf59c0\", \"name\": \"CRS-26\", \"date_utc\": \"2022-11-18T22:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"633f71820531f07b4fdf59bd\", \"name\": \"Starlink 4-37 (v1.5)\", \"date_utc\": \"2022-11-01T00:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6243ba08af52800c6e919270\", \"name\": \"O3b mPower 1,2\", \"date_utc\": \"2022-11-01T00:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"633f724c0531f07b4fdf59c5\", \"name\": \"SWOT\", \"date_utc\": \"2022-12-05T00:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"633f72000531f07b4fdf59c2\", \"name\": \"SES-18 & SES-19\", \"date_utc\": \"2022-11-01T00:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"633f72580531f07b4fdf59c6\", \"name\": \"Transporter-6\", \"date_utc\": \"2022-12-01T00:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"63161384ffc78f3b8567070e\", \"name\": \"TTL-1\", \"date_utc\": \"2022-12-01T00:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6243ae58af52800c6e91925a\", \"name\": \"WorldView Legion 1 & 2\", \"date_utc\": \"2022-12-01T00:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"633f72130531f07b4fdf59c3\", \"name\": \"Viasat-3 & Arcturus\", \"date_utc\": \"2022-12-01T00:00:00.000Z\"}}\n",
            "{\"type\": \"RECORD\", \"stream\": \"launches\", \"record\": {\"id\": \"6243ae7daf52800c6e91925b\", \"name\": \"O3b mPower 3.4\", \"date_utc\": \"2022-12-01T00:00:00.000Z\"}}\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# test l'extracteur\n",
        "!python tap_spacex.py > output.json"
      ],
      "metadata": {
        "id": "7O69fa0MN-vV",
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "outputId": "a7e9b65c-81bb-4dd6-a531-8a6724f48563"
      },
      "execution_count": 9,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "python3: can't open file '/content/tap_spacex.py': [Errno 2] No such file or directory\n"
          ]
        }
      ]
    }
  ]
}