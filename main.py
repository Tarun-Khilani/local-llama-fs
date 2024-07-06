import asyncio
import click

from app.loader import load_documents
from app.summarizer import get_dir_summaries
from app.tree_generator import generate_file_tree
from app.utils import create_file_tree, save_file_tree


@click.command()
@click.argument("src_path", type=click.Path(exists=True))
@click.argument("dst_path", type=click.Path())
@click.option("--auto-yes", is_flag=True, help="Automatically say yes to all prompts")
def main(src_path, dst_path, auto_yes=False):
    # Load docs
    docs = load_documents(src_path)

    # Get directory summaries
    summaries = asyncio.run(get_dir_summaries(docs, src_path))

    # Get file tree
    file_tree = generate_file_tree(summaries)

    updated_file_tree = create_file_tree(file_tree, src_path, dst_path)

    if not auto_yes and not click.confirm(
        "Proceed with directory structure?", default=True
    ):
        click.echo("Operation cancelled.")
        return

    save_file_tree(updated_file_tree)


if __name__ == "__main__":
    main()