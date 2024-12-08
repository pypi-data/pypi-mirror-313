import logging

import click

from datapools.api import crawl
from datapools.common.logger import logger, setup_logger


class NotRequiredIf(click.Option):
    def __init__(self, *args, **kwargs):
        self.not_required_if = kwargs.pop("not_required_if")
        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs["help"] = (
            kwargs.get("help", "") + " NOTE: This argument is mutually exclusive with %s" % self.not_required_if
        ).strip()
        super(NotRequiredIf, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        we_are_present = self.name in opts
        other_present = self.not_required_if in opts

        if other_present:
            if we_are_present:
                raise click.UsageError(
                    "Illegal usage: `%s` is mutually exclusive with `%s`" % (self.name, self.not_required_if)
                )
            else:
                self.prompt = None

        return super(NotRequiredIf, self).handle_parse_result(ctx, opts, args)


def main():
    # (hint_urls, config_file ) = cli_init(standalone_mode=False)
    try:
        (id, config_file) = cli_init(standalone_mode=False)
        logger.info("cli_init done")
        # await crawl( hint_urls, config_file )
        crawl(id, config_file)
        logger.info("crawl done")
    except KeyboardInterrupt as e:
        logger.info("exiting")


@click.group(invoke_without_command=True)
@click.option(
    "-l",
    "--loglevel",
    type=str,
    default="info",
    help="info, debug, error, warning}}",
)
@click.option("--config-file", type=str, help="todo", default=None)
# @click.option("-u", "--hint-url", type=str, multiple=True)
# @click.option("--hint-urls-file", type=str)
@click.option("--id", type=int, help="datapool id", default=1)
@click.pass_context
def cli_init(ctx, **kwargs):
    """parsing command line and return arguments for datapools.crawl() call"""
    level = logging.getLevelName(kwargs.get("loglevel").upper())
    setup_logger(level)
    # print(logger)

    # TODO: exclusive options should be processed by click
    # hint_url = kwargs.get("hint_url")
    # if hint_url:
    #     hint_urls = {hint_url}
    # else:
    #     hint_urls_file = kwargs.get("hint_urls_file")
    #     if hint_urls_file:
    #         with open(hint_urls_file, "r") as f:
    #             lines = f.readlines()
    #             hint_urls = set()
    #             for line in lines:
    #                 line = line.strip()
    #                 if len(line):
    #                     hint_urls.add(line)
    #     else:
    #         raise Exception("Expect --hint-url or --hint-urls-file argument(s)")
    id = kwargs.get("id")

    config_file = kwargs.get("config_file")
    # return (hint_urls, config_file)
    return (id, config_file)
