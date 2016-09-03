---
type: post
categories: config
tags: [ code, factures, geek, github, hack, latex  ]
title: "Gestion des factures en autoentrepreneur"
date: 2012-02-06T18:05:12+02:00
summary: "Je me suis depuis peu inscrit au statut auto-entrepreneur, et évidemment, j'ai vite eu besoin de sortir une facture. J'ai cherché sur le net, et ai trouvé deux blogs qui ont fait un système identique Tengu en suisse et Godefroy en France. Dans la suite de l'article, les sources LaTeX."
lang: francais
logo: /img/facture.png
header_background: /img/stackofpapers.jpeg
aliases:
 - /hack/on/gestion-des-factures-en-autoentrepreneur/
---

Je me suis depuis peu inscrit au statut auto-entrepreneur, et évidemment,
j'ai vite eu besoin de sortir une facture. J'ai cherché sur le net, et ai
trouvé deux blogs qui ont fait un système identique [Tengu](https://blog.tengu.ch/blog/post/47)
en suisse et [Godefroy](http://godefroy.me/latex-comment-faire-rapidement-une-facture-super-classe-a530591) 
en France.

Bref, j'ai repris leur travail et l'ai adapté au besoin d'autoentrepreneurs
(que des factures HT et la mention qui va bien), et fait quelques modifs comme 
notamment revenir à la font originelle qui est plus belle que la « bera » (quelle
horreur), fait en sorte que la compilation se fasse à l'aide d'un simple "make" et
d'avoir toutes les factures rangées, .tex/.pdf cote à cote.

Tout ça est sur mon [github](https://github.com/guyzmo/facturation_latex) comme d'hab !
