
library(icd.data)
df <- icd.data::icd9cm_hierarchy
print(head(df, 10))

write.table(df,
            file="data/tmp/allcodes.csv",
            sep="|")


chapters <- icd.data::icd9_chapters
write.table(chapters,
            file = "data/tmp/chapters.csv",
            sep="|")

subchapters <- icd.data::icd9_sub_chapters
write.table(subchapters,
            file = "data/tmp/subchapters.csv",
            sep="|")


majors <- icd.data::icd9_majors
write.table(majors,
            file = "data/tmp/majors.csv",
            sep="|")