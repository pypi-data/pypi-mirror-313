## 1.28.1 - 2024-12-07
### Extractors
#### Additions
- [bluesky] add `info` extractor
#### Fixes
- [bluesky] fix exception when encountering non-quote embeds ([#6577](https://github.com/mikf/gallery-dl/issues/6577))
- [bluesky] unescape search queries ([#6579](https://github.com/mikf/gallery-dl/issues/6579))
- [common] restore using environment proxy settings by default ([#6553](https://github.com/mikf/gallery-dl/issues/6553), [#6609](https://github.com/mikf/gallery-dl/issues/6609))
- [common] improve handling of `user-agent` settings ([#6594](https://github.com/mikf/gallery-dl/issues/6594))
- [e621] fix `TypeError` when `metadata` is enabled ([#6587](https://github.com/mikf/gallery-dl/issues/6587))
- [gofile] fix website token extraction ([#6596](https://github.com/mikf/gallery-dl/issues/6596))
- [inkbunny] fix re-login loop ([#6618](https://github.com/mikf/gallery-dl/issues/6618))
- [instagram] handle empty `carousel_media` entries ([#6595](https://github.com/mikf/gallery-dl/issues/6595))
- [kemonoparty] fix `o` query parameter handling ([#6597](https://github.com/mikf/gallery-dl/issues/6597))
- [nhentai] fix download URLs ([#6620](https://github.com/mikf/gallery-dl/issues/6620))
- [readcomiconline] fix `chapter` extraction ([#6070](https://github.com/mikf/gallery-dl/issues/6070), [#6335](https://github.com/mikf/gallery-dl/issues/6335))
- [realbooru] fix extraction ([#6543](https://github.com/mikf/gallery-dl/issues/6543))
- [rule34] fix `favorite` extraction ([#6573](https://github.com/mikf/gallery-dl/issues/6573))
- [zerochan] download `.webp` and `.gif` files ([#6576](https://github.com/mikf/gallery-dl/issues/6576))
#### Improvements
- [hentaicosplays] update domains ([#6578](https://github.com/mikf/gallery-dl/issues/6578))
- [pixiv:ranking] implement filtering results by `content` ([#6574](https://github.com/mikf/gallery-dl/issues/6574))
- [pixiv] include user ID in failed AJAX request warnings ([#6581](https://github.com/mikf/gallery-dl/issues/6581))
#### Options
- [patreon] add `format-images` option ([#6569](https://github.com/mikf/gallery-dl/issues/6569))
- [zerochan] add `extensions` option ([#6576](https://github.com/mikf/gallery-dl/issues/6576))
