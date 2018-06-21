#!/usr/bin/env bash
curl http://0.0.0.0:8000/crawler/detik/list &&
curl http://0.0.0.0:8000/crawler/kompas/list &&
curl http://0.0.0.0:8000/crawler/kompas/detail &&
curl http://0.0.0.0:8000/crawler/detik/news-type &&
curl http://0.0.0.0:8000/crawler/detik/detail/singlepagenews