## ----setup, include=FALSE-----------------------------------------------------
knitr::opts_chunk$set(echo = TRUE, message = FALSE, warning = FALSE)

## ----strTSE, echo=FALSE, fig.width= 12, fig.cap= "The structure of the TreeSummarizedExperiment class."----
knitr::include_graphics("tse2.png")

## -----------------------------------------------------------------------------
library(TreeSummarizedExperiment)

# assays data (typically, representing observed data from an experiment)
assay_data <- rbind(rep(0, 4), matrix(1:20, nrow = 5))
colnames(assay_data) <- paste0("sample", 1:4)
rownames(assay_data) <- paste("entity", seq_len(6), sep = "")
assay_data

## -----------------------------------------------------------------------------
# row data (feature annotations)
row_data <- data.frame(Kingdom = "A",
                       Phylum = rep(c("B1", "B2"), c(2, 4)),
                       Class = rep(c("C1", "C2", "C3"), each = 2),
                       OTU = paste0("D", 1:6),
                       row.names = rownames(assay_data),
                       stringsAsFactors = FALSE)

row_data
# column data (sample annotations)
col_data <- data.frame(gg = c(1, 2, 3, 3),
                       group = rep(LETTERS[1:2], each = 2), 
                       row.names = colnames(assay_data),
                       stringsAsFactors = FALSE)
col_data

## -----------------------------------------------------------------------------
library(ape)

# The first toy tree 
set.seed(12)
row_tree <- rtree(5)

# The second toy tree 
set.seed(12)
col_tree <- rtree(4)

# change node labels
col_tree$tip.label <- colnames(assay_data)
col_tree$node.label <- c("All", "GroupA", "GroupB")

## ----plot-rtree, fig.cap="\\label{plot-rtree} The structure of the row tree. The node labels and the node numbers are in orange and blue text, respectively.", out.width="90%"----
library(ggtree)
library(ggplot2)

# Visualize the row tree
ggtree(row_tree, size = 2, branch.length = "none") +
    geom_text2(aes(label = node), color = "darkblue",
               hjust = -0.5, vjust = 0.7, size = 5.5) +
    geom_text2(aes(label = label), color = "darkorange",
               hjust = -0.1, vjust = -0.7, size = 5.5) 

## ----plot-ctree, fig.cap="\\label{plot-ctree} The structure of the column tree. The node labels and the node numbers are in orange and blue text, respectively.", out.width="90%"----
# Visualize the column tree
ggtree(col_tree, size = 2, branch.length = "none") +
    geom_text2(aes(label = node), color = "darkblue",
               hjust = -0.5, vjust = 0.7, size = 5.5) +
    geom_text2(aes(label = label), color = "darkorange",
               hjust = -0.1, vjust = -0.7, size = 5.5)+
    ylim(c(0.8, 4.5)) +
    xlim(c(0, 2.2))

## -----------------------------------------------------------------------------
# all column names could be found in the node labels of the column tree
all(colnames(assay_data) %in% c(col_tree$tip.label, col_tree$node.label))

# provide the node labels in rowNodeLab
tip_lab <- row_tree$tip.label
row_lab <- tip_lab[c(1, 1:5)]
row_lab

both_tse <- TreeSummarizedExperiment(assays = list(Count = assay_data),
                                     rowData = row_data,
                                     colData = col_data,
                                     rowTree = row_tree,
                                     rowNodeLab = row_lab,
                                     colTree = col_tree)

## -----------------------------------------------------------------------------
both_tse

## -----------------------------------------------------------------------------
# to get the first table in the assays
(count <- assays(both_tse)[[1]])

## -----------------------------------------------------------------------------
# to get row data
rowData(both_tse)

## -----------------------------------------------------------------------------
# to get column data
colData(both_tse)

## -----------------------------------------------------------------------------
# to get metadata: it's empty here
metadata(both_tse)

## -----------------------------------------------------------------------------
# get trees
rowTree(both_tse)
colTree(both_tse)

## -----------------------------------------------------------------------------
new_tse <- both_tse

# a new tree
new_tree <- rtree(nrow(new_tse))
new_tree$tip.label <- rownames(new_tse)

# the original row tree is replaced with the new tree
rowTree(new_tse) <- new_tree
identical(rowTree(new_tse), rowTree(both_tse))
identical(rowTree(new_tse), new_tree)


## -----------------------------------------------------------------------------
# access the link data
(r_link <- rowLinks(both_tse))
(c_link <- colLinks(both_tse))

## -----------------------------------------------------------------------------
class(r_link)
showClass("LinkDataFrame")

## -----------------------------------------------------------------------------
refSeq <- DNAStringSet(rep("AGCT", nrow(both_tse)))

## -----------------------------------------------------------------------------
referenceSeq(both_tse) <- refSeq
referenceSeq(both_tse)

## -----------------------------------------------------------------------------
both_tse

## -----------------------------------------------------------------------------
sub_tse <- both_tse[1:2, 1]
sub_tse

# The tree stays the same
identical(rowTree(sub_tse), rowTree(both_tse))

## -----------------------------------------------------------------------------
# the row data
rowData(sub_tse)

# the row link data
rowLinks(sub_tse)


## -----------------------------------------------------------------------------
# The first four columns are from colLinks data and the others from colData
cbind(colLinks(sub_tse), colData(sub_tse))

## -----------------------------------------------------------------------------
node_tse <- subsetByNode(x = both_tse, rowNode = "t3")

rowLinks(node_tse)

## -----------------------------------------------------------------------------
node_tse <- subsetByNode(x = both_tse, rowNode = "t3", 
                         colNode = c("sample1", "sample2"))
assays(node_tse)[[1]]

## ----plot-taxa2phylo, fig.cap="\\label{plot-taxa2phylo} The structure of the taxonomic tree that is generated from the taxonomic table.", out.width="90%"----
# The toy taxonomic table
(taxa <- rowData(both_tse))

# convert it to a phylo tree
taxa_tree <- toTree(data = taxa)

# Viz the new tree
ggtree(taxa_tree)+
    geom_text2(aes(label = node), color = "darkblue",
               hjust = -0.5, vjust = 0.7, size = 5.5) +
    geom_text2(aes(label = label), color = "darkorange",
               hjust = -0.1, vjust = -0.7, size = 5.5) +
    geom_point2()

## -----------------------------------------------------------------------------
taxa_tse <- changeTree(x = both_tse, rowTree = taxa_tree, 
                       rowNodeLab = taxa[["OTU"]])

taxa_tse
rowLinks(taxa_tse)

## -----------------------------------------------------------------------------
# use node labels to specify colLevel
agg_col <- aggTSE(x = taxa_tse,
                  colLevel = c("GroupA", "GroupB"),
                  colFun = sum)

# or use node numbers to specify colLevel
agg_col <- aggTSE(x = taxa_tse, colLevel = c(6, 7), colFun = sum)

## -----------------------------------------------------------------------------
assays(agg_col)[[1]]

## -----------------------------------------------------------------------------
# before aggregation
colData(taxa_tse)
# after aggregation
colData(agg_col)

## -----------------------------------------------------------------------------
agg_col <- aggTSE(x = taxa_tse, colLevel = c(6, 7),
                  colFun = sum, colDataCols = "group")
colData(agg_col)

## -----------------------------------------------------------------------------
# the link data is updated
colLinks(agg_col)

## -----------------------------------------------------------------------------
# the phylum level
taxa <- c(taxa_tree$tip.label, taxa_tree$node.label)
(taxa_one <- taxa[startsWith(taxa, "Phylum:")])

# aggregation
agg_taxa <- aggTSE(x = taxa_tse, rowLevel = taxa_one, rowFun = sum)
assays(agg_taxa)[[1]]

## -----------------------------------------------------------------------------
# A mixed level
taxa_mix <- c("Class:C3", "Phylum:B1")
agg_any <- aggTSE(x = taxa_tse, rowLevel = taxa_mix, rowFun = sum)
rowData(agg_any)

## -----------------------------------------------------------------------------
agg_both <- aggTSE(x = both_tse, colLevel = c(6, 7), 
                   rowLevel = 7:9, rowFun = sum,
                   colFun = mean, rowFirst = FALSE)

## -----------------------------------------------------------------------------
assays(agg_both)[[1]]

## ----plot-exTree, fig.cap= "\\label{plot-exTree} An example tree with node labels and numbers in black and orange texts, respectively.", out.width="90%"----
data("tinyTree")
ggtree(tinyTree, branch.length = "none") +
    geom_text2(aes(label = label), hjust = -0.1, size = 5.5) +
    geom_text2(aes(label = node), vjust = -0.8,
               hjust = -0.2, color = 'orange', size = 5.5) 

## -----------------------------------------------------------------------------
convertNode(tree = tinyTree, node = c(12, 1, 4))

## -----------------------------------------------------------------------------
convertNode(tree = tinyTree, node = c("t4", "Node_18"))

## -----------------------------------------------------------------------------
# only the leaf nodes
findDescendant(tree = tinyTree, node = 17, only.leaf = TRUE)

## -----------------------------------------------------------------------------
# all descendant nodes
findDescendant(tree = tinyTree, node = 17, only.leaf = FALSE)

## -----------------------------------------------------------------------------
# tse: a TreeSummarizedExperiment object
# rowLeaf: specific leaves
subsetByLeaf <- function(tse, rowLeaf) {
  # if rowLeaf is provided as node labels, convert them to node numbers
  if (is.character(rowLeaf)) {
    rowLeaf <- convertNode(tree = rowTree(tse), node = rowLeaf)
  }
  
  # subset data by leaves
  sse <- subsetByNode(tse, rowNode = rowLeaf)
  
  # update the row tree
    ## -------------- new tree: drop leaves ----------
    oldTree <- rowTree(sse)
    newTree <- ape::keep.tip(phy = oldTree, tip = rowLeaf)
    
    ## -------------- update the row link ----------
    # track the tree
    track <- trackNode(oldTree)
    track <- ape::keep.tip(phy = track, tip = rowLeaf)
    
    # row links
    rowL <- rowLinks(sse)
    rowL <- DataFrame(rowL)
    
    # update the row links: 
    #   1. use the alias label to track and updates the nodeNum
    #   2. the nodeLab should be updated based on the new tree using the new
    #      nodeNum
    #   3. lastly, update the nodeLab_alias
    rowL$nodeNum <- convertNode(tree = track, node = rowL$nodeLab_alias,
                              message = FALSE)
    rowL$nodeLab <- convertNode(tree = newTree, node = rowL$nodeNum, 
                              use.alias = FALSE, message = FALSE)
    rowL$nodeLab_alias <- convertNode(tree = newTree, node = rowL$nodeNum, 
                                    use.alias = TRUE, message = FALSE)
    rowL$isLeaf <- isLeaf(tree = newTree, node = rowL$nodeNum)

    rowNL <- new("LinkDataFrame", rowL)
    
    ## update the row tree and links
    BiocGenerics:::replaceSlots(sse,
                              rowLinks = rowNL,
                              rowTree = list(phylo = newTree))
}


## -----------------------------------------------------------------------------
(both_sse <- subsetByLeaf(tse = both_tse, rowLeaf = c("t2", "t3")))
rowLinks(both_sse)

## -----------------------------------------------------------------------------
sessionInfo()

