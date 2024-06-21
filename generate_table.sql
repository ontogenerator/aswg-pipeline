create table papers (
    id integer primary key generated always as identity,
    filename text unique,
    discussion_text text,
    methods_text text,
    all_text text,
    jet_page_numbers json,
    limitation_sentences json,
    trial_numbers json,
    sciscore json,
    is_modeling_paper boolean,
    graph_types json,
    is_open_data boolean,
    is_open_code boolean,
    reference_check json,
    coi_statement boolean,
    funding_statement boolean,
    registration_statement boolean
)
