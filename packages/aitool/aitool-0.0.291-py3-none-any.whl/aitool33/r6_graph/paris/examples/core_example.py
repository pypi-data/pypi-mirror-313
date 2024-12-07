import os
from aitool import get_aitool_data, print_green, print_yellow
from aitool.r6_graph.paris.tool.dataloader import construct_kg
from aitool.r6_graph.paris.objects.KGs import KGs


def alignment(
        relation_triples_path_1,
        attribute_triples_path_1,
        relation_triples_path_2,
        attribute_triples_path_2,
        ent_links_path,
        output_file,
        iteration_number=3,
):
    kg1 = construct_kg(relation_triples_path_1, attribute_triples_path_1)
    kg2 = construct_kg(relation_triples_path_2, attribute_triples_path_2)
    kgs = KGs(kg1=kg1, kg2=kg2, iteration=iteration_number)
    # kgs.util.load_embedding(ent_emb_path, kg1_emb_indices_path, kg2_emb_indices_path)
    kgs.util.load_ent_links(path=ent_links_path)
    kgs.run(test_path=ent_links_path)
    kgs.util.save_results(path=output_file)


def core_example(data_dir, output_file, iteration_number=3):
    relation_triples_path_1 = os.path.join(data_dir, 'rel_triples_1')
    attribute_triples_path_1 = os.path.join(data_dir, 'attr_triples_1')
    relation_triples_path_2 = os.path.join(data_dir, 'rel_triples_2')
    attribute_triples_path_2 = os.path.join(data_dir, 'attr_triples_2')
    ent_links_path = os.path.join(data_dir, 'ent_links')

    alignment(
        relation_triples_path_1,
        attribute_triples_path_1,
        relation_triples_path_2,
        attribute_triples_path_2,
        ent_links_path,
        output_file,
        iteration_number=iteration_number,
    )


def core_example_en_de_15k(iteration_number=3):
    data_dir = get_aitool_data('EN_DE_15K_V1', sub_path='r6_graph', packed=True,
                               packed_name='EN_DE_15K_V1.zip', pack_way='zip')
    output_file = './ent_links_EN_DE_15K_V1_iter{}'.format(iteration_number)
    print_green('Example of PARIS, using EN_DE_15K_V1 dataset')
    print_yellow('data_dir: ', data_dir)
    print_yellow('output_file: ', output_file)
    core_example(data_dir, output_file, iteration_number=iteration_number)


def core_example_zh_industry_med(iteration_number=3):
    data_dir = get_aitool_data('ZH_INDUSTRY_Med', sub_path='r6_graph', packed=True,
                               packed_name='ZH_INDUSTRY_Med.zip', pack_way='zip')
    output_file = './ent_links_ZH_INDUSTRY_Med_iter{}'.format(iteration_number)
    print_green('Example of PARIS, using ZH_INDUSTRY_Med dataset')
    print_yellow('data_dir: ', data_dir)
    print_yellow('output_file: ', output_file)
    core_example(data_dir, output_file, iteration_number=iteration_number)


if __name__ == '__main__':
    # core_example_en_de_15k()
    core_example_zh_industry_med(iteration_number=1)
