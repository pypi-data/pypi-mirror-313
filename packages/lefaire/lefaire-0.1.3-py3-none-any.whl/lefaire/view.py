from colorama import Fore, Style
from datetime import datetime


def labelize(str):
    label = str.rjust(16) + " : "
    return dim(label)


def justify(str):
    justified = str.rjust(16) + " - "
    return justified


def margin(str):
    return " ".rjust(13) + str


def projectNum(id):
    return f"{id}".zfill(3)


def taskNum(id):
    return f"{id}".zfill(2)


def dim(str):
    dimmed = Style.DIM + str + Style.RESET_ALL
    return dimmed


def green(str):
    colored = Fore.GREEN + str + Style.RESET_ALL
    return colored


def yellow(str):
    colored = Fore.YELLOW + str + Style.RESET_ALL
    return colored


def blue(str):
    colored = Fore.BLUE + str + Style.RESET_ALL
    return colored


def red(str):
    colored = Fore.RED + str + Style.RESET_ALL
    return colored


def success(str):
    msg = green("\nOK!\n") + str + "\n"
    print(msg)


def warning(str):
    msg = yellow("\nATTENTION !\n") + str
    return msg


def safe(str):
    msg = blue("\nPAS DE PANIQUE !\n") + str + "\n"
    print(msg)


def error(e):
    str = f"{e}"
    msg = red("\nOupsy...\n" + str + "\n")
    print(msg)


def toFrenchDate(mysqlDate):
    if mysqlDate:
        return mysqlDate.strftime("%d/%m/%Y %H:%M:%S")
    return None


def toUSDate(frenchDate):
    return datetime.strptime(frenchDate, "%d/%m/%Y %H:%M:%S")


def show_status(obj, long: bool = False):
    if long:
        status = "À faire"
        if obj.started:
            status = yellow("En cours  ")
        if obj.isComplete:
            status = green("Terminé  ")
    else:
        status = " "
        if obj.started:
            status = yellow(" ")
        if obj.isComplete:
            status = green(" ")
    return status


def main_header():
    text = "Projets"

    return "\n" + dim(margin(text)) + "\n"


def project_header(project):
    id = projectNum(project.ID)
    name = project.name
    description = project.description
    if not description:
        description = dim("Ajouter une description 'lefaire description [projectID]'")
    header = justify(id) + name
    subHeader = labelize("Description") + description
    return "\n\n" + header + "\n" + subHeader


def projects(projectList):
    todo = []
    done = []
    for project in projectList:
        box = show_status(project)
        id = projectNum(project.ID)
        name = project.name
        line = justify(id) + box + " " + name
        if project.isComplete:
            done.append(line)
        else:
            todo.append(line)

    if todo:
        todo.append("\n")
    if done:
        done.append("\n")

    view = "\n".join(todo) + "\n".join(done)
    return view


def list(projectList):
    view = main_header()
    if projectList:
        view += projects(projectList)
    else:
        view += dim(
            "Vous n'avez pas encore de projets.\nAjoutez-en avec la commande `create`"
        )
    print(view)


def tasks(taskList):
    todo = []
    done = []
    if not taskList:
        placeholder = (
            "\n"
            + labelize("Tâches")
            + dim(
                "Ce projet n'a encore aucune tâche. Pour ajouter un tâche 'lefaire add [projectID]'\n"
            )
        )
        return placeholder
    for task in taskList:
        box = show_status(task)
        rank = taskNum(task.rank)
        body = task.body
        if task.isComplete:
            line = dim(justify(rank)) + box + " " + dim(body)
            done.append(line)
        else:
            line = justify(rank) + dim(box) + " " + body
            todo.append(line)
    if todo:
        todo.append("\n")
    if done:
        done.append("\n")

    view = "\n" + "\n".join(todo) + "\n".join(done)
    return view


def project_info(project, taskList):
    header = project_header(project) + "\n"
    status = labelize("Statut") + show_status(project, True) + "\n"
    created = labelize("Crée le") + toFrenchDate(project.created) + "\n"
    if project.started:
        started = labelize("Commencé le") + toFrenchDate(project.started) + "\n"
    else:
        started = labelize("Commencé le") + dim(
            "Pour commencer un projet, commencer une de ses tâches 'lefaire start [projectID] [rank]'\n"
        )

    if project.completionDate:
        completionDate = (
            labelize("Terminé le") + toFrenchDate(project.completionDate) + "\n"
        )
        completionTime = labelize("Durée totale") + str(
            project.completionDate - project.started
        )
        completion = completionDate + completionTime + "\n"
    else:
        completion = labelize("Terminé le") + dim(
            "Pour compléter un projet, compléter toutes ses tâches 'lefaire done [projectID] [rank]'\n"
        )
    if project.dueDate:
        dueDate = labelize("Date butoir") + toFrenchDate(project.dueDate) + "\n"
    else:
        dueDate = labelize("Date butoir") + dim(
            "Ajouter une date butoir 'lefaire due [projectID]'\n"
        )
    subtasks = tasks(taskList)
    infos = header + status + created + dueDate + started + completion + subtasks
    print(infos)


def task_info(task):
    rank = taskNum(task.rank)
    header = justify(rank) + task.body + "\n"
    status = labelize("Statut") + show_status(task, True) + "\n"
    created = labelize("Crée le") + toFrenchDate(task.created) + "\n"
    if task.started:
        started = labelize("Commencé le") + toFrenchDate(task.started) + "\n"
    else:
        started = labelize("Commencé le") + dim(
            "Commencer une tâche 'lefaire start [taskID] [rank]'\n"
        )
    if task.completionDate:
        completionDate = (
            labelize("Terminé le") + toFrenchDate(task.completionDate) + "\n"
        )
        completionTime = labelize("Durée totale") + str(
            task.completionDate - task.started
        )
        completion = completionDate + completionTime + "\n"
    else:
        completion = labelize("Terminé le") + dim(
            "Compléter une tâche 'lefaire done [projectID] [rank]"
        )
    infos = "\n" + header + status + created + started + completion + "\n"
    print(infos)


def create(project):
    return success(
        "Le projet "
        + projectNum(project.ID)
        + " - "
        + green(project.name)
        + " a bien été créé !"
    )


def rename(nb, name):
    return success(
        "Le projet " + projectNum(nb) + f" a bien été renommé '{green(name)}'."
    )


def relocate(project):
    return success(
        f"Le projet {green(project.name)} porte désormais le numéro {green(projectNum(project.ID))}."
    )


def desc(project):
    return success(
        f"La description du projet {projectNum(project.ID)} - '{green(project.name)}' a bien été modifiée."
    )


def due(project):
    return success(
        f"La date butoir du projet {projectNum(project.ID)} - '{green(project.name)}' a bien été modifiée."
    )


def add(task, project):
    return success(
        f"La tâche {green(task.body)} a bien été ajoutée au projet '{green(project.name)}'."
    )


def edit(task, project):
    return success(
        f"La tâche n°{task.rank} du projet {projectNum(project.ID)} - '{green(project.name)}' a bien été renommée '{green(task.body)}'."
    )


def start(task, project):
    return success(
        f"La tâche '{green(task.body)}' du projet {projectNum(project.ID)} - '{green(project.name)}' a bien été commencée."
    )


def unstart(task, project):
    return success(
        f"La tâche '{green(task.body)}' du projet {projectNum(project.ID)} - '{green(project.name)}' a bien été arrêtée."
    )


def complete(task, project):
    return success(
        f"La tâche '{green(task.body)}' du projet {projectNum(project.ID)} - '{green(project.name)}' a bien été terminée."
    )


def commit_cmd(task):
    return f"\n git add . && git commit -m '{task.body}'"


def commit_prompt(cmd):
    return warning(
        f"On est dans le {yellow('bon dossier')} ?\nOn peut exécuter la commande : {yellow(cmd)} ? "
    )


def commit_success():
    return success(f"La commande a bien été {green('exécutée')}")


def uncomplete(task, project):
    return success(
        f"La tâche '{green(task.body)}' du projet {projectNum(project.ID)} - '{green(project.name)}' n'est pas terminée."
    )


def move(task, project, dir):
    print(dir.lower())
    if dir.lower() == "up":
        dir = "vers le haut"
    elif dir.lower() == "down":
        dir = "vers le bas"
    elif dir.lower() == "top":
        dir = "tout en haut"
    else:
        dir = "tout en bas"

    return success(
        f"La tâche '{green(task.body)}' du projet {projectNum(project.ID)} - '{green(project.name)}' a bien été déplacée {dir}."
    )


def delete_task(task, project):
    return success(
        f"La tâche '{green(task.body)}' du projet {projectNum(project.ID)} - '{green(project.name)}' a bien été supprimée."
    )


def delete_project(project):
    return success(
        f"Le projet {projectNum(project.ID)} - '{green(project.name)}' a bien été supprimé."
    )


def delete_all_prompt():
    return warning(f"Voulez-vous supprimer un projet en {yellow('ENTIER')} ?")


def delete_task_warning(task, project):
    return warning(
        f"La tâche '{yellow(task.body)}' du projet '{yellow(project.name)}' est sur le point d'être supprimée.\n\nContinuer ? "
    )


def delete_project_warning(project):
    return warning(
        f"Le projet  '{yellow(project.name)}' est sur le point d'être supprimé.\n\nContinuer ? "
    )


def delete_task_safe(task, project):
    return safe(
        f"La tâche '{blue(task.body)}' du projet '{blue(project.name)}' est conservée."
    )


def delete_project_safe(project):
    return safe(f"Le projet  '{blue(project.name)}' est conservé.")
