# aswg-pipeline

We are the [Automated Screening Working Group](https://scicrunch.org/ASWG), a group of researchers aiming to improve 
scientific manuscripts on a large scale. Our pipeline combines tools that check for common problems in scientific
manuscripts to produce a single, integrated report for any paper.

# Overview

Our pipeline offers a unified framework for retrieval and preprocessing of papers, a pluggable interface for tools,
and formatting and public release of tool results as a unified report. While we encourage developers to experiment with 
and add their own tools, we are currently using the following tools in our production pipeline:

 * [JetFighter](https://github.com/smsaladi/jetfighter)
 * [limitation-recognizer](https://github.com/kilicogluh/limitation-recognizer)
 * [trial-identifier](https://github.com/bgcarlisle/TRNscreener)
 * [SciScore](https://sciscore.com/)
 * [Barzooka](https://github.com/NicoRiedel/barzooka)
 * [ODDPub](https://github.com/quest-bih/oddpub)
 * [rtransparent](https://github.com/serghiou/rtransparent)

## Publications

[*Automated screening of COVID-19 preprints: can we help authors to improve transparency and reproducibility?*](https://www.nature.com/articles/s41591-020-01203-7) in *Nature Medicine*.