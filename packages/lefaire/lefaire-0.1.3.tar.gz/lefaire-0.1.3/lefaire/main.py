import typer
import os
import lefaire.view as view
import lefaire.data as data
from typing_extensions import Annotated

app = typer.Typer()
move_app = typer.Typer()
app.add_typer(move_app, name="move", help="Déplacer une tâche dans la liste de tâche.")


@app.command()
def add(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    body: Annotated[str, typer.Argument(help="Corps de la tâche")] = "",
    top: Annotated[
        bool,
        typer.Option(
            "-t",
            "--top",
            help="Est-ce que la tâche est à mettre tout en haut de la pile ?",
        ),
    ] = False,
):
    """
    Ajouter une tâche.
    """
    conn = data.db_connect()
    cur = conn.cursor()

    try:
        if not num:
            list()
            num = typer.prompt("À quel projet ajouter une tâche ? ")

        if not body:
            list(num)
            body = typer.prompt("En quoi consiste cette tâche ? ")
        task = data.add_task(cur, num, body)
        conn.commit()
        if top:
            data.move_ext(cur, num, task.rank, "top")
            conn.commit()
            task = data.get_task_by_ID(cur, task.ID)
        project = data.get_single_project(cur, num)
        view.add(task, project)
        conn.close()
        info(num)

    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


@app.command()
def create(
    name: Annotated[str, typer.Argument(help="Nom du projet")] = "",
    description: Annotated[str, typer.Argument(help="Description du projet")] = "",
):
    """
    Créer un projet.
    """
    conn = data.db_connect()
    cur = conn.cursor()
    try:
        if not name:
            name = typer.prompt("Quel est le nom de ce nouveau projet ? ")
        project = data.create_project(cur, name, description)
        view.create(project)
        conn.commit()
        conn.close()
        list()

    except NameError as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


@app.command()
def delete(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
    all: Annotated[bool, typer.Option("-a", "--all", "-p", "--project")] = False,
):
    """
    Supprimer un projet. Pour supprimer une tâche, ajouter son rang
    """
    try:
        if not (all or rang):
            all = typer.confirm(view.delete_all_prompt())

        if all:
            delete_project(num)
        else:
            delete_task(num, rang)

    except Exception as e:
        view.error(e)
        raise typer.Exit()


def delete_project(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    conn = data.db_connect()
    cur = conn.cursor()
    if not num:
        list()
        num = typer.prompt("Quel projet voulez-vous supprimer ? ")
    project = data.get_single_project(cur, num)
    confirm = typer.confirm(view.delete_project_warning(project))
    if confirm:
        data.delete_project(cur, num)
        conn.commit()
        view.delete_project(project)
    else:
        view.delete_project_safe(project)

    conn.close()
    list()


def delete_task(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    conn = data.db_connect()
    cur = conn.cursor()

    if not num:
        list()
        num = typer.prompt("Dans quel projet se trouve la tâche à supprimer ? ")

    if not rang:
        list(num)
        rang = typer.prompt("Quelle tâche doit être supprimée ? ")

    task = data.get_single_task(cur, num, rang)
    project = data.get_single_project(cur, num)

    confirm = typer.confirm(view.delete_task_warning(task, project))
    if confirm:
        data.delete_task(cur, task.ID)
        view.delete_task(task, project)
        conn.commit()
    else:
        view.delete_task_safe(task, project)
    conn.close()
    info(num)


@app.command()
def desc(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    description: Annotated[str, typer.Argument(help="Description du projet")] = "",
):
    """
    Ajouter ou modifier la description d'un projet.
    """
    conn = data.db_connect()
    cur = conn.cursor()

    try:
        if not num:
            list()
            num = typer.prompt("Quel projet est à modifier ? ")

        if not description:
            list(num)
            description = typer.prompt("Comment décrire le projet ? ")

        project = data.update_description(cur, num, description)
        view.desc(project)
        conn.commit()
        conn.close()
        info(num)

    except Exception as e:
        view.error(e)
        raise typer.Exit()
        conn.close()


@app.command()
def done(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
    commit: Annotated[bool, typer.Option("-g", "-c", "--git", "--commit")] = False,
):
    """
    Marquer une tâche comme terminée.
    """
    conn = data.db_connect()
    cur = conn.cursor()
    try:
        if not num:
            list()
            num = typer.prompt("À quel projet appartient la tâche à terminer ? ")

        if not rang:
            list(num)
            rang = typer.prompt("Quel est le rang de la tâche à terminer? ")

        project = data.get_single_project(cur, num)
        task = data.complete_task(cur, num, rang)
        conn.commit()
        view.complete(task, project)

        # add to git command to clipboard
        cmd = view.commit_cmd(task)
        if commit:
            sure = True
        else:
            sure = typer.confirm(view.commit_prompt(cmd))
        if sure:
            os.system(cmd)
            view.commit_success()

        info(num)
        conn.close()

    except Exception as e:
        view.error(e)
        raise typer.Exit()
        conn.close()


@app.command()
def due(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    date: Annotated[str, typer.Argument(help="Date butoir du projet")] = "",
):
    """
    Ajouter ou modifier une date butoir (JJ/MM/AAA HH:MM:SS).
    """
    conn = data.db_connect()
    cur = conn.cursor()

    try:
        if not num:
            list()
            num = typer.prompt("Quel projet est à modifier ? ")

        if not date:
            list(num)
            date = typer.prompt("Quelle est la date butoir pour ce projet ? ")

        date = view.toUSDate(date)
        project = data.update_due_date(cur, num, date)
        view.due(project)
        conn.commit()
        conn.close()
        info(num)

    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


@app.command()
def edit(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
    body: Annotated[str, typer.Argument(help="Corps de la tâche")] = "",
):
    """
    Modifier le corps d'une tâche.
    """
    conn = data.db_connect()
    cur = conn.cursor()

    try:
        if not num:
            list()
            num = typer.prompt("À quel projet appartient la tâche à modifier ? ")

        if not rang:
            list(num)
            rang = typer.prompt("Quel est le rang de la tâche à modifier ? ")

        if not body:
            list(num, rang)
            body = typer.prompt("En quoi consiste cette tâche ? ")
        project = data.get_single_project(cur, num)
        task = data.update_body(cur, num, rang, body)
        view.edit(task, project)
        conn.commit()
        conn.close()
        info(num)

    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


def list(num: int = 0, rang: int = 0):
    """
    Lister les projets.
    """
    conn = data.db_connect()
    cur = conn.cursor()
    try:
        if rang:
            task = data.get_single_task(cur, num, rang)
            view.task_info(task)
        elif num:
            project = data.get_single_project(cur, num)
            taskList = data.clean_ranks(cur, num)
            view.project_info(project, taskList)
        else:
            projectsList = data.get_projects(cur)
            view.list(projectsList)

    except Exception as e:
        view.error(e)
        raise typer.Exit()

    conn.close()


def project_menu(num):
    choice = typer.prompt(
        "(A)jouter une tâche | (I)nfo d'une tâche | (R)enommer | Changer la (D)escription | Changer la date (B)utoir | (S)upprimer | (Q)uitter "
    )

    choice = choice.lower()
    if choice == "a":
        add(num)
    elif choice == "i":
        rang = typer.prompt("Quel est le rang de la tâche à consulter ? ")
        info(num, rang)
    elif choice == "r":
        rename(num)
    elif choice == "d":
        desc(num)
    elif choice == "b":
        due(num)
    elif choice == "s":
        delete(num, "", True)
    elif choice == "q":
        print("\n")
    else:
        try:

            int(choice)
            conn = data.db_connect()
            cur = conn.cursor()
            data.get_single_task(cur, num, choice)
        except Exception as e:
            pass
            view.error(e)
        else:
            info(num, choice)


def task_menu(num, rang):
    conn = data.db_connect()
    cur = conn.cursor()
    rang = int(rang)
    task = data.get_single_task(cur, num, rang)
    menu = "(E)diter | "
    if not task.started:
        menu += "(C)ommencer | "
    if task.started and not task.isComplete:
        menu += "(A)rrêter | "
    if not task.isComplete:
        menu += "(T)erminer | "
    if task.isComplete:
        menu += "(R)etravailler | "
    menu += "(D)éplacer | (S)upprimer | (Q)uitter "

    choice = typer.prompt(menu)
    choice = choice.lower()
    if choice == "e":
        edit(num, rang)
    if choice == "c":
        start(num, rang)
    if choice == "a":
        unstart(num, rang)
    if choice == "t":
        done(num, rang)
    if choice == "r":
        undo(num, rang)
    if choice == "d":
        dir = typer.prompt(
            "Déplacer vers le (H)aut | Déplacer vers le (B)as | Mettre en (P)remier | Mettre en (D)ernier "
        )
        dir = dir.lower()
        if dir == "h":
            dir = "up"
        if dir == "b":
            dir = "down"
        if dir == "p":
            dir = "top"
        if dir == "d":
            dir = "bottom"
        move(dir, num, rang)
    if choice == "s":
        delete(num, rang)
    if choice == "q":
        info(num)


@app.command()
def info(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Détailler les infos sur un projet.
    """
    try:
        if rang:
            list(num, rang)
            task_menu(num, rang)
        elif num:
            list(num)
            project_menu(num)
        else:
            list()
            num = typer.prompt("Entrer le numéro du projet à consulter ")
            info(num)

    except Exception as e:
        view.error(e)
        raise typer.Exit()


@app.command()
def relocate(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    new: Annotated[int, typer.Argument(help="Nouveau numéro du projet")] = 0,
):
    """
    Changer le numéro d'identifiant d'un projet
    """
    conn = data.db_connect()
    cur = conn.cursor()

    try:
        if not num:
            list()
            num = typer.prompt("Quel projet est à deplacer ? ")

        if not new:
            new = typer.prompt("Quel est le nouvel identifiant de ce projet ? ")

        project = data.relocate_project(cur, num, new)
        view.relocate(project)
        conn.commit()
        conn.close()
        list()
    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


@app.command()
def rename(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    name: Annotated[str, typer.Argument(help="Nouveau nom du projet")] = "",
):
    """
    Renommer un projet.
    """
    conn = data.db_connect()
    cur = conn.cursor()

    try:
        if not num:
            list()
            num = typer.prompt("Quel projet est à renommer ? ")

        if not name:
            name = typer.prompt("Quel est le nouveau nom de ce projet ? ")

        data.rename_project(cur, num, name)
        view.rename(num, name)
        conn.commit()
        conn.close()
        list()
    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


@app.command()
def start(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Marquer une tâche comme commencée.
    """
    conn = data.db_connect()
    cur = conn.cursor()

    try:
        if not num:
            list()
            num = typer.prompt("À quel projet appartient la tâche à commencer ? ")

        if not rang:
            list(num)
            rang = typer.prompt("Quel est le rang de la tâche à commencer ? ")

        project = data.get_single_project(cur, num)
        task = data.start_task(cur, num, rang)
        view.start(task, project)
        conn.commit()
        conn.close()
        info(num)

    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


@app.command()
def test():
    os.system("python ~/Code/sanctu/lefaire/test_data.py")


@app.command()
def undo(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Marquer une tâche comme non terminée.
    """
    conn = data.db_connect()
    cur = conn.cursor()
    try:
        if not num:
            list()
            num = typer.prompt("À quel projet appartient la tâche à retravailler ? ")

        if not rang:
            list(num)
            rang = typer.prompt("Quel est le rang de la tâche à retravailler ? ")

        project = data.get_single_project(cur, num)
        task = data.uncomplete_task(cur, num, rang)
        view.uncomplete(task, project)
        conn.commit()
        conn.close()
        info(num)

    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


@app.command()
def unstart(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Marquer une tâche comme non commencée.
    """
    conn = data.db_connect()
    cur = conn.cursor()
    try:
        if not num:
            list()
            num = typer.prompt("À quel projet appartient la tâche à arrêter ? ")

        if not rang:
            list(num)
            rang = typer.prompt("Quel est le rang de la tâche à arrêter ? ")

        project = data.get_single_project(cur, num)
        task = data.unstart_task(cur, num, rang)
        view.unstart(task, project)
        conn.commit()
        conn.close()
        info(num)

    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


def move(
    dir: Annotated[str, typer.Argument(help="Direction")],
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Déplacer une tâche dans la liste de tâche.
    """
    conn = data.db_connect()
    cur = conn.cursor()

    try:
        if not num:
            list()
            num = typer.prompt("À quel projet appartient la tâche à déplacer ? ")

        if not rang:
            list(num)
            rang = typer.prompt("Quel est le rang de la tâche à déplacer ? ")
            rang = int(rang)

        task = data.get_single_task(cur, num, rang)
        project = data.move(cur, num, rang, dir)
        view.move(task, project, dir)
        conn.commit()
        conn.close()
        info(num)

    except Exception as e:
        view.error(e)
        conn.close()
        raise typer.Exit()


@move_app.command("up")
def move_up(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Déplacer une tâche vers le haut dans la liste de tâche.
    """
    move("up", num, rang)


@move_app.command("down")
def move_down(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Déplacer une tâche vers le bas dans la liste de tâche
    """
    move("down", num, rang)


@move_app.command("top")
def move_top(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Déplacer une tâche tout en haut de la liste de tâche.
    """
    move("top", num, rang)


@move_app.command("bottom")
def move_bottom(
    num: Annotated[int, typer.Argument(help="Numéro du projet")] = 0,
    rang: Annotated[int, typer.Argument(help="Rang de la tâche")] = 0,
):
    """
    Déplacer une tâche tout en vas de la liste de tâche.
    """
    move("bottom", num, rang)


if __name__ == "__main__":
    app()
