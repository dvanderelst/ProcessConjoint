library(ez)
library(xtable)
library(apaTables)
library(psychReport)

#----------------------------------------------------
data<-read.csv('jurgen_within_data.csv')
ezPlot(data, dv=Rating, split=Actor, x=Action, row = Malady, wid=ResponseId, between = c(Malady,Action), within=Actor)
result <- ezANOVA(data, dv=Rating , wid=ResponseId, between = c(Malady, Action), within=Actor)
output = '/home/dieter/Dropbox/Apps/Overleaf/RobotsAndNurses/output/LM_jurgen_2.tex'
#apa.ezANOVA.table(result, correction = "GG", table.title = "", output, table.number = NA)

tex <-printTable(result$ANOVA, caption = NA, digits = 2, onlyContents = FALSE)
tex <-sub("\\caption\\{NA\\}", "", tex)
tex <-gsub("longtable", "tabular\\", tex)

fileConn<-file(output)
writeLines(tex, fileConn)
close(fileConn)

