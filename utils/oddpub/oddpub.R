library(furrr)
future::plan(multisession)
args <- commandArgs(TRUE)
pdf_folder <- args[1]
print(pdf_folder)
text_folder <- "temp/oddpub_text/"
print(text_folder)
#pdf_files <- list.files(pdf_folder, pattern = "pdf|PDF", full.names = TRUE)
#file.copy(pdf_files, text_folder)
#conversion_success <- pdf_convert(text_folder, text_folder)
conversion_success <- oddpub::pdf_convert(pdf_folder, text_folder)
list.files(pdf_folder)[!conversion_success]
PDF_text_sentences <- oddpub::pdf_load(text_folder)
#PDF_text_sentences <- oddpub::pdf_load(args[1])
open_data_results <- oddpub::open_data_search(PDF_text_sentences)
write.table(open_data_results, file=args[2])
