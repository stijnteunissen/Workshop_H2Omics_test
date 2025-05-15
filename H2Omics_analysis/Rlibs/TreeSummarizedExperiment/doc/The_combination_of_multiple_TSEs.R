## ----setup, include=FALSE-----------------------------------------------------
knitr::opts_chunk$set(echo = TRUE, message = FALSE, warning = TRUE)

## -----------------------------------------------------------------------------
library(TreeSummarizedExperiment)

set.seed(1)
# TSE: without the column tree
(tse_a <- makeTSE(include.colTree = FALSE))

# combine two TSEs by row
(tse_aa <- rbind(tse_a, tse_a))

## -----------------------------------------------------------------------------
identical(rowTree(tse_aa), rowTree(tse_a))

## -----------------------------------------------------------------------------
set.seed(2)
tse_b <- makeTSE(include.colTree = FALSE)

# different row trees
identical(rowTree(tse_a), rowTree(tse_b))

# 2 phylo tree(s) in rowTree
(tse_ab <- rbind(tse_a, tse_b))

## -----------------------------------------------------------------------------
rowLinks(tse_aa)
rowLinks(tse_ab)

## -----------------------------------------------------------------------------
rowTreeNames(tse_aa)
rowTreeNames(tse_ab)

# The original tree names in the input TSEs
rowTreeNames(tse_a)
rowTreeNames(tse_b)

## -----------------------------------------------------------------------------
rowTreeNames(tse_ab) <- paste0("tree", 1:2)
rowLinks(tse_ab)

## -----------------------------------------------------------------------------
cbind(tse_a, tse_a)
cbind(tse_a, tse_b)

## -----------------------------------------------------------------------------
(sse <- tse_ab[11:15, ])
rowLinks(sse)

## -----------------------------------------------------------------------------
set.seed(3)
tse_c <- makeTSE(include.colTree = FALSE)
rowTreeNames(tse_c) <- "new_tree"

# the first two rows are from tse_c, and are mapped to 'new_tree'
sse[1:2, ] <- tse_c[5:6, ]
rowLinks(sse)

## -----------------------------------------------------------------------------
# by tree
sse_a <- subsetByNode(x = sse, whichRowTree = "new_tree")
rowLinks(sse_a)

# by node
sse_b <- subsetByNode(x = sse, rowNode = 5)
rowLinks(sse_b)

# by tree and node
sse_c <- subsetByNode(x = sse, rowNode = 5, whichRowTree = "tree2")
rowLinks(sse_c)

## -----------------------------------------------------------------------------
colTree(sse)

library(ape)
set.seed(1)
col_tree <- rtree(ncol(sse))

# To use 'colTree` as a setter, the input tree should have node labels matching
# with column names of the TSE.
col_tree$tip.label <- colnames(sse)

colTree(sse) <- col_tree
colTree(sse)

## -----------------------------------------------------------------------------
# the original row links
rowLinks(sse)

# the new row tree
set.seed(1)
row_tree <- rtree(4)
row_tree$tip.label <- paste0("entity", 5:7)

# replace the tree named as the 'new_tree'
nse <- sse
rowTree(nse, whichTree = "new_tree") <- row_tree
rowLinks(nse)

## -----------------------------------------------------------------------------
# FALSE is expected
identical(rowTree(sse, whichTree = "new_tree"),
          rowTree(nse, whichTree = "new_tree"))

# TRUE is expected
identical(rowTree(nse, whichTree = "new_tree"),
          row_tree)

## -----------------------------------------------------------------------------
sessionInfo()

