description = {
    "AIDS": " Human immunodeficiency virus (HIV) is an infection that attacks the body's immune system."
            " Acquired immunodeficiency syndrome (AIDS) is the most advanced stage of the disease. HIV"
            " targets the body's white blood cells, weakening the immune system."
}


def get_decs_utils(x):
    desc = description.get(x, '')
    return desc

