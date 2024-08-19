import pickle
from collections import defaultdict


symbol_dict = {'green': '<td class="icon-column"><img src="green.png" width="40"></td>  ',
               'yellow': '<td class="icon-column"><img src="yellow.png" width="40"></td>  ',
               'red': '<td class="icon-column"><img src="red.png" width="40"></td>  ',
               'gray': '<td class="icon-column"><img src="gray.png" width="40"></td>  ',
               'info': '<a href="_LINK_"><img src="info.png" width="20"></a>  '}
symbol_dict_no_col = {'green': '<img src="green.png" width="40">  ',
                      'yellow': '<img src="yellow.png" width="40">  ',
                      'red': '<img src="red.png" width="40">  ',
                      'gray': '<img src="gray.png" width="40">  ',
                      'info': '<a href="_LINK_"><img src="info.png" width="20"></a>  '}

links = {'IRB': 'https://hyp.is/P1lOfhJTEe282zPFUo_Viw/www.scicrunch.com/sciscorereport-faq',
         'Consent': 'https://hyp.is/RQGGrBJTEe2T_9-B3PrCtA/www.scicrunch.com/sciscorereport-faq',
         'IACUC': 'https://hyp.is/UBZy0hJTEe2Qq2Nw6ZpCPw/www.scicrunch.com/sciscorereport-faq',
         'Field Permit': 'https://hyp.is/WriqthJTEe2Q3x8XQ2FRsQ/www.scicrunch.com/sciscorereport-faq',
         'Euthanasia': 'https://hyp.is/ZIx_1hJTEe2zsVOs1ci3Sw/www.scicrunch.com/sciscorereport-faq',
         'Inclusion and Exclusion Criteria': 'https://hyp.is/bsuuLBJTEe2SYcOLv0aQjA/www.scicrunch.com/sciscorereport-faq',
         'flow charts': 'https://scicrunch.org/ASWG/about/ToolTips#flowcharts',
         'Attrition': 'https://hyp.is/ZnR5DhJWEe2somsB3dMc0g/www.scicrunch.com/sciscorereport-faq',
         'Sex as a biological variable': 'https://hyp.is/bU8a6hJWEe2KzPOyfjTFfw/www.scicrunch.com/sciscorereport-faq',
         'Age': 'https://hyp.is/eAPlxBJWEe27dleoY9naPg/www.scicrunch.com/sciscorereport-faq',
         'Weight': 'https://hyp.is/gLvkRhJWEe2G83cnpms8PQ/www.scicrunch.com/sciscorereport-faq',
         'Randomization': 'https://hyp.is/h844uhJWEe2j9muTwTqFBw/www.scicrunch.com/sciscorereport-faq',
         'Blinding': 'https://hyp.is/jvlXZBJWEe284rOrv3lDAA/www.scicrunch.com/sciscorereport-faq',
         'Power Analysis': 'https://hyp.is/lQ3deBJWEe2-4tveyW_TXA/www.scicrunch.com/sciscorereport-faq',
         'Replication': 'https://hyp.is/m1YX4BJWEe2zumdAdd7tgQ/www.scicrunch.com/sciscorereport-faq',
         'Cell Line Authentication': 'https://hyp.is/qJd6AhJWEe2fCsO7wUR7fA/www.scicrunch.com/sciscorereport-faq',
         'Cell Line Contamination': 'https://hyp.is/rvAyhhJWEe2knvOtM_RVwg/www.scicrunch.com/sciscorereport-faq',
         'Antibodies': 'https://hyp.is/FnytDhJbEe2PJkP1lk8NJw/www.scicrunch.com/sciscorereport-faq',
         'Experimental Models: Cell Lines': 'https://hyp.is/HJssxBJbEe2X-xfr4qKBTA/www.scicrunch.com/sciscorereport-faq',
         'Experimental Models: Organisms/Strains': 'https://hyp.is/I8jRXhJbEe2UE9Mj94sJUg/www.scicrunch.com/sciscorereport-faq',
         'Plasmids': 'https://hyp.is/KljkvhJbEe2sr08Ts79L_Q/www.scicrunch.com/sciscorereport-faq',
         'Software and Algorithms': 'https://hyp.is/MIreRhJbEe2fE4do8-8MEg/www.scicrunch.com/sciscorereport-faq',
         'open code': 'https://datascience.codata.org/articles/10.5334/dsj-2020-042/',
         'code identifiers': 'https://hyp.is/tWI4WBJWEe2SaVdACeu9Mw/www.scicrunch.com/sciscorereport-faq',
         'open data': 'https://datascience.codata.org/articles/10.5334/dsj-2020-042/',
         'data identifiers': 'https://hyp.is/vObNPBJWEe2bmG-YJRUNmQ/www.scicrunch.com/sciscorereport-faq',
         'registration': 'https://scicrunch.org/ASWG/about/ToolTips#registrationstatement',
         'protocol identifiers': 'https://hyp.is/w9xcdBJWEe2fC3dXFukpLQ/www.scicrunch.com/sciscorereport-faq',
         'coi': 'https://doi.org/10.1371/journal.pbio.3001107',
         'limitations': 'https://doi.org/10.1093%2Fjamia%2Focy038',
         'bar graphs': 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8947810/',
         'dot plots': 'https://twitter.com/T_Weissgerber/status/1192694947385876480',
         'original bar paper': 'https://pubmed.ncbi.nlm.nih.gov/25901488/',
         'rainbow colormaps': 'https://elifesciences.org/labs/c2292989/jetfighter-towards-figure-accuracy-and-accessibility',
         'funding': 'https://www.medrxiv.org/content/10.1101/2022.04.11.22273744v1.full-text',
         'Recombinant DNA': ''}

tool_links = {'SciScore': 'https://sciscore.com/',
              'ODDPub': 'https://datascience.codata.org/article/10.5334/dsj-2020-042/',
              'limitation-recognizer': 'https://pubmed.ncbi.nlm.nih.gov/29718377/',
              'rtransparent': 'https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3001107',
              'trial-identifier': 'https://github.com/bgcarlisle/TRNscreener',
              'JetFighter': 'https://elifesciences.org/labs/c2292989/jetfighter-towards-figure-accuracy-and-accessibility',
              'Barzooka': 'https://portlandpress.com/clinsci/article/136/15/1139/231562/Replacing-bar-graphs-of-continuous-data-with-more'}


def tool_specifier(tool_str):
    if tool_str.find(' (') > 0:
        return(tool_str.split(' (')[0])
    else: return(tool_str)


def generate_table(rows, name, tools, resources_table=False, explanation='', limitations=''):
    tools = [f'<a href="{tool_links[tool_specifier(tool)]}"">{tool}</a>' for tool in tools]
    table = ''
    if resources_table:
        rows = [list(row) for row in rows]
        i = 0
        while i < len(rows):
            if rows[i][0] == '':
                rows[i - 1][2] += '<br>' + rows[i][2]
                del rows[i]
            else:
                i += 1
        for row in rows:
            table += f"<tr><td class='description-column'>{row[0]}</td><td class='sentence-column'>{row[1]}</td><td>{row[2]}</td></tr>"
    else:
        for row in rows:
            symbol = symbol_dict[row[0]]
            if len(row) == 2:
                table += f"<tr>{symbol}<td class='description-column'>{row[1]}</td></tr>"
            else:
                table += f"<tr>{symbol}<td class='description-column'>{row[1]}</td><td>{row[2]}</td></tr>"
    return f'<h2>{name}</h2>{explanation}<table>{table}</table><i>Generated by {", ".join(tools)}</i>.<br>{limitations}'


def generate_html(doi, filename, jetfighter, limitation_recognizer, trial_identifier, sciscore, barzooka, oddpub, rtransparent):
    html = ''
    after_html = ''
    rows = []

    # reference check
    #critical = False
    #if reference_check[doi]['raw_json']['status'] == 'FAILURE':
    #rows = [('gray', 'Retracted references; References with erratums or corrections.', f"{symbol_dict['info'].replace('_LINK_', links['scite ref check'])}Tool failure.")]
    #else:
    #    rows = []
    #    for citation_doi in reference_check[doi]['raw_json']['papers']:
    #        if 'retracted' in reference_check[doi]['raw_json']['papers'][citation_doi]:
    #            title = reference_check[doi]['raw_json']['papers'][citation_doi]['title']
    #            title = title[:60] + ('…' if len(title) > 60 else '')
    #            if reference_check[doi]['raw_json']['papers'][citation_doi]['retracted'] == True or reference_check[doi]['raw_json']['papers'][citation_doi]['retracted'] == 'Retracted':
    #                critical = True
    #                rows.append((2, 'Retracted', f'''A paper you reference, {citation_doi} ("{title}"), has been retracted. If you need to cite this paper, we recommend noting at the beginning of the citation that the paper is retracted (i.e. RETRACTED: Title of paper, authors, journal, etc.).'''))
    #            elif isinstance(reference_check[doi]['raw_json']['papers'][citation_doi]['retracted'], str) and ['Has erratum', 'Has correction', 'Has expression of concern'] in reference_check[doi]['raw_json']['papers'][citation_doi]['retracted']:
    #                rows.append((1, 'Has erratum', f'''A paper you reference, {citation_doi} ("{title}"), has an erratum posted. We recommend checking the erratum to confirm that it does not impact the accuracy of your citation.'''))
    #    if not rows:
    #        rows = [('green', 'Retracted references; References with erratums or corrections.', f"{symbol_dict['info'].replace('_LINK_', links['scite ref check'])}We found no retracted references, and no references with erratums or corrections.")]
    #if critical:
    #    html += generate_table(rows, 'Critical issues (references)', ['scite.ai'])
    #else:
    #    after_html += generate_table(rows, 'References', ['scite.ai'])

    # rigor
    if sciscore[doi]['is_modeling_paper']:
        html += f'<h2>Rigor</h2>NIH rigor criteria are not applicable to paper type.<br><i>Generated by <a href="{tool_links["SciScore"]}">SciScore</a></i>'
    else:
        if trial_identifier[doi]['trial_identifiers']:
            alert = 'green'
            bullets = []
            for trial in trial_identifier[doi]['trial_identifiers']:
                if trial['link']:
                    bullets.append(f"<a href=\"{trial['link']}\">{trial['identifier']}</a>: {trial['status']}")
                else:
                    bullets.append(f"{trial['identifier']}: {trial['status']}")
                if not (trial['resolved'] or 'ISRCTN' in trial['identifier']):
                    alert = 'red'
                    bullets[-1] += ' (Trial number did not resolve on <a href="https://clinicaltrials.gov/">clinicaltrials.gov</a>. Is the number correct?)'
                    bullets[-1] = f'<a style="color:red">{bullets[-1]}</a>'
                bullets[-1] = f'<li>{bullets[-1]}</li>'
            rows.append((alert, 'Clinical trial numbers', f"The following clinical trial numbers were referenced:<br><ul>{''.join(bullets)}</ul>"))
        else:
            rows.append(('green', 'Clinical trial numbers', 'No clinical trial numbers were referenced.'))
        rows = []
        for sr in sciscore[doi]['raw_json']['rigor-table']['sections']:
            if sr['title'] == 'Attrition':
                alert = 'yellow'
                if barzooka[doi]['graph_types']['flowyes']:
                    text = symbol_dict['info'].replace('_LINK_', links['flow charts']) + 'Thank you for including a study flow chart and information about attrition and exclusions to help readers evaluate the risk of bias.'
                    alert = 'green'
                else:
                    text = symbol_dict['info'].replace('_LINK_', links['flow charts']) + 'We did not find a study flow chart of excluded observations. We strongly recommend using flow charts because they provide an overview of the study design and more information about attrition. If you included a study flow chart in your supplemental files, we apologize for missing this. Our tool is not able to screen separate supplemental files.'
                if sr['srList'][0]['sentence'] in ('not detected.', 'not required.'):
                    text += f"<br><br>{symbol_dict['info'].replace('_LINK_', links['Attrition'])}Sentence about attrition: {sr['srList'][0]['sentence']}"
                else:
                    text += f"<br><br>{symbol_dict['info'].replace('_LINK_', links['Attrition'])}Sentence about attrition: <i>\"{sr['srList'][0]['sentence']}\"</i>"
                rows.append((alert, 'Flow charts and attrition', text))
            else:
                if sr['srList'][0]['sentence'] == 'not detected.':
                    alert = 'yellow'
                elif sr['srList'][0]['sentence'] == 'not required.':
                    alert = 'gray'
                else:
                    for sentence in sr['srList']:
                        sentence['sentence'] = '<i>"' + sentence['sentence'] + '</i>"'
                    alert = 'green'
                rows.append([alert, sr['title'], (symbol_dict['info'].replace('_LINK_', links[sr['title']]) if sr['title'] in links else '') + '<br>'.join([((((symbol_dict['info'].replace('_LINK_', links[s['title']] if s['title'] in links else '')) + s['title'] + ': ') if 'title' in s else '') + s['sentence']) for s in sr['srList']])])
        html += generate_table(rows, 'Rigor', ['Barzooka (flow charts)', 'SciScore (everything else)'], resources_table=False, limitations='SciScore only screens the text of the methods section; we apologize if the tool has missed items reported elsewhere in the paper or supplements.')

    # sciscore resources
    if len(sciscore[doi]['raw_json']['sections']) == 0:
        html += f'<h2>Resources</h2>No key resources detected.<br><i>Generated by <a href="{tool_links["SciScore"]}">SciScore</a>. SciScore only screens the text of the methods section; we apologize if the tool has missed items reported elsewhere in the paper or supplements.</i>'
    else:
        rows = []
        for section in sciscore[doi]['raw_json']['sections']:
            sentences = []
            mentions = defaultdict(list)
            for item in section['srList']:
                sentence = item['sentence']
                sentences.append(sentence)
                for mention in item['mentions']:
                    identifier = mention['rrid']
                    detected = True
                    if identifier is None:
                        if 'suggestedRrid' in mention.keys():
                            identifier = mention['suggestedRrid']
                        detected = False
                    identifier = str(identifier)
                    identifier = identifier.replace(')', '')
                    if 'RRID:' in identifier:
                        rrid = identifier.split('RRID:')[1].strip().replace(')', '')
                        identifier = identifier.replace('RRID:', 'RRID:<a href="https://n2t.net/RRID:') + '">' + rrid + '</a>)'
                    note = ''
                    term = mention['neText']
                    if detected:
                        term = symbol_dict_no_col['green'] + term
                    elif identifier == 'None':
                        term = symbol_dict_no_col['yellow'] + term
                        note = 'Please add an <a href="https://scicrunch.org/resources">RRID</a> to help others identify this resource.'
                    else:
                        term = symbol_dict_no_col['yellow'] + term
                        note = 'Please make sure this RRID suggestion is accurate before including in your manuscript.'
                    mentions[sentence].append({'term': term, 'identifier': identifier, 'detected': detected, 'note': note})
            prev_sentence = ''
            for sentence in sentences:
                for mention in mentions[sentence]:
                    col1 = symbol_dict_no_col['info'].replace('_LINK_', links[section['sectionName']]) + section['sectionName']
                    if (col1 + sentence) == prev_sentence:
                        sentence = ''
                    else:
                        prev_sentence = col1 + sentence
                    if mention['detected']:
                        if sentence:
                            rows.append((col1, '<i>"' + sentence + '"</i>', f"{mention['term']} found: {mention['identifier'].replace(')', '')}."))
                        else:
                            rows.append(('', '', f"{mention['term']} found: {mention['identifier'].replace(')', '')}."))
                    else:
                        if sentence:
                            rows.append((col1, '<i>"' + sentence + '"</i>', f"{mention['term']} suggested: {mention['identifier'].replace(')', '')}. {mention['note']}"))
                        else:
                            rows.append(('', '', f"{mention['term']} suggested: {mention['identifier'].replace(')', '')}. {mention['note']}"))
        html += generate_table(rows, 'Resources', ['SciScore'], resources_table=True, explanation='Persistent unique identifiers for research resources, RRIDs, can be used to track these key resources though the literature. They are requested or required in many journals, but even if your journal does not require them, we strongly encourage the use of these for the readers of papers who wish to easily track down the key materials like antibodies, software tools, or mice.',
         limitations='SciScore only screens the text of the methods section; we apologize if the tool has missed items reported elsewhere in the paper or supplements.')

    # transparency
    rows = []
    try:
        if oddpub[doi]['open_code']:
            rows.append(('green', 'Open code', symbol_dict['info'].replace('_LINK_', links['open code']) + f"<i>\"{oddpub[doi]['open_code_statement']}\"</i>"))
        else:
            rows.append(('yellow', 'Open code', symbol_dict['info'].replace('_LINK_', links['open code']) + 'If you wrote code to analyze your data, please consider sharing the code in a public repository. This makes it easier for others to reproduce your analyses, and may also aid others seeking to analyze similar datasets.'))
        if oddpub[doi]['open_data']:
            rows.append(('green', 'Open data', symbol_dict['info'].replace('_LINK_', links['open data']) + f"<i>\"{oddpub[doi]['open_data_statement']}\"</i>"))
        else:
            rows.append(('yellow', 'Open data', symbol_dict['info'].replace('_LINK_', links['open data']) + 'If permitted, sharing data can improve reproducibility and make it easier for other scientists to expand on your work. Papers with open data are cited more often than papers without open data. Some institutions have an expert who can provide advice on data sharing.'))
    except:
        rows.append(('yellow', 'Open code', symbol_dict['info'].replace('_LINK_', links['open code']) + 'If you wrote code to analyze your data, please consider sharing the code in a public repository. This makes it easier for others to reproduce your analyses, and may also aid others seeking to analyze similar datasets.'))
        rows.append(('yellow', 'Open data', symbol_dict['info'].replace('_LINK_', links['open data']) + 'If permitted, sharing data can improve reproducibility and make it easier for other scientists to expand on your work. Papers with open data are cited more often than papers without open data. Some institutions have an expert who can provide advice on data sharing.'))
    limitations = ' '.join(limitation_recognizer[doi]['sents']).replace('  ', ' ')
    if limitations:
        rows.append(('green', 'Self-acknowledged limitations', symbol_dict['info'].replace('_LINK_', links['limitations']) + f'<i>\"{limitations[:1000]}{"..." if len(limitations) > 1000 else ""}\"</i>'))
    else:
        rows.append(('yellow', 'Self-acknowledged limitations', symbol_dict['info'].replace('_LINK_', links['limitations']) + 'An explicit section about the limitations of this study was not found. We encourage authors to include a paragraph in the discussion that addresses study limitations. Every study has limitations. Describing these limitations helps readers to understand and contextualize the research.'))
    if rtransparent[doi]['coi_statement']:
        rows.append(('green', 'Conflict of interest statement', symbol_dict['info'].replace('_LINK_', links['coi']) + 'Thank you for stating any conflicts of interest.'))
    else:
        rows.append(('yellow', 'Conflict of interest statement', symbol_dict['info'].replace('_LINK_', links['coi']) + 'It is important to supply a conflict of interest statement, even if there are none to declare, to transparently present the research.'))
    if rtransparent[doi]['funding_statement']:
        rows.append(('green', 'Funding statement', symbol_dict['info'].replace('_LINK_', links['funding']) + 'Thank you for reporting your funding source(s), or stating that there was no specific funding for this work.'))
    else:
        rows.append(('yellow', 'Funding statement', symbol_dict['info'].replace('_LINK_', links['funding']) + 'It is important to supply a funding statement because it makes the funding source and potential conflicts of interests transparent.'))
    if rtransparent[doi]['registration_statement']:
        rows.append(('green', 'Registration statement', symbol_dict['info'].replace('_LINK_', links['registration']) + 'Thank you for registering your study.'))
    else:
        rows.append(('gray', 'Registration statement', symbol_dict['info'].replace('_LINK_', links['registration']) + 'A registered protocol makes the planned research project more transparent and can protect against bias. Please consider registering future confirmatory studies.'))
    html += generate_table(rows, 'Transparency', ['ODDPub', 'limitation-recognizer', 'rtransparent', 'trial-identifier'])
    
    # figures
    rows = []
    if barzooka[doi]['graph_types']['bar']:
        rows.append(('yellow', 'Bar graphs of continuous data', symbol_dict['info'].replace('_LINK_', links['bar graphs']) + f'We found bar graphs of continuous data. We recommend replacing these with more informative graphics (e.g. dotplots, box plots, violin plots), as many different datasets can lead to the same bar graph. The actual data may suggest different conclusions from the summary statistics alone. Please see the following resources for more information on the problems with bar graphs <a href={links["original bar paper"]}>(Weissgerber et al 2015)</a> and what to use instead <a href={links["bar graphs"]}>(Weissgerber et al 2019)</a>.'))
    else:
        rows.append(('green', 'No bar graphs of continuous data', symbol_dict['info'].replace('_LINK_', links['bar graphs']) + 'Thank you for not using bar graphs to present continuous data. Many different datasets and data distributions can lead to the same bar graph, and the actual data may suggest different conclusions from the summary statistics alone.'))
    if barzooka[doi]['graph_types']['bardot']:
        rows.append(('yellow', 'Bar graphs with dot plots', symbol_dict['info'].replace('_LINK_', links['dot plots']) + 'Thank you for showing individual data points on your bar graphs. We recommend removing the bars and showing only a dot plot. The resource linked in the information symbol illustrates several reasons why dot plots are better than bar graphs with dot plots.'))
    if jetfighter[doi]['page_nums']:
        rows.append(('yellow', 'Rainbow color maps', symbol_dict['info'].replace('_LINK_', links['rainbow colormaps']) + f'Please consider replacing  the rainbow (“jet”) colormap(s) that we detected in at least one figure with alternatives like Viridis or Cividis. Rainbow color maps distort readers’ perception of the data by introducing visual artifacts. Rainbow color maps are  also inaccessible to readers with colorblindness. Alternatives colormaps like Viridis and Cividis are accessible to colorblind readers and avoid visual artifacts.'))
    else:
        rows.append(('green', 'No rainbow color maps', symbol_dict['info'].replace('_LINK_', links['rainbow colormaps']) + 'Thank you for not using rainbow colormaps. Rainbow color maps distort readers’ perception of the data by introducing visual artifacts and are not accessible to colorblind readers.'))
    html += generate_table(rows, 'Figures', ['JetFighter', 'Barzooka'])

    html = open('base.html', 'r').read().replace('_PAPER_ID_', filename).replace('_TABLES_', html + after_html)
    return html
