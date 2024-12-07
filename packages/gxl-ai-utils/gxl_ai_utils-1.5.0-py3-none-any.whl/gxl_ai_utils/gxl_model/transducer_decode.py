from .transducer_search import greedy_search


def greedy_search_for_one_batch(input_x, x_lens, model):
    """

    :param input_x:
    :param input_lens:
    :param model:
    :return:
    """
    encoder_outputs, x_lens = model.encoder(input_x, x_lens)
    batch_size = encoder_outputs.size(0)
    res_list = []
    for i in range(batch_size):
        encoder_output_now = encoder_outputs[i:i+1]
        encoder_output_now = encoder_output_now[:, :x_lens[i], :]
        hyp = greedy_search(model, encoder_output_now)
        res_list.append(hyp)
    return res_list


def test_greedy_search():
    """"""



