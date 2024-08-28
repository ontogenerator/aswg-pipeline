library(furrr)
future::plan(multisession)
args <- commandArgs(TRUE)
pdf_folder <- args[1]
print(pdf_folder)
text_folder <- "temp/oddpub_text/"
print(text_folder)
conversion_success <- oddpub::pdf_convert(pdf_folder, text_folder)
list.files(pdf_folder)[!conversion_success]
PDF_text_sentences <- oddpub::pdf_load(text_folder)
open_data_results <- oddpub::open_data_search(PDF_text_sentences)
write.table(open_data_results, file=args[2])

