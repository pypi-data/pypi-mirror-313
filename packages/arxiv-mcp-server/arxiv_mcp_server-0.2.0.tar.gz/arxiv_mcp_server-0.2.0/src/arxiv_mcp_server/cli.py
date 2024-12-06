import asyncio
import argparse
import sys

from .server import ServiceFactory, SearchParameters


def parse_args():
    parser = argparse.ArgumentParser(
        description="Search and analyze arXiv papers from the command line"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for papers on arXiv")
    search_parser.add_argument("query", help="Search query string")
    search_parser.add_argument(
        "--max-results",
        type=int,
        default=10,
        help="Maximum number of results (default: 10)",
    )
    search_parser.add_argument(
        "--date-from", help="Filter papers from this date (YYYY-MM-DD)"
    )
    search_parser.add_argument(
        "--date-to", help="Filter papers until this date (YYYY-MM-DD)"
    )
    search_parser.add_argument(
        "--categories", nargs="+", help="Filter by arXiv categories (e.g., cs.AI cs.LG)"
    )
    search_parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="Number of papers to process in each batch (default: 10)",
    )

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze", help="Get detailed analysis of a specific paper"
    )
    analyze_parser.add_argument("paper_id", help="arXiv paper ID")

    return parser.parse_args()


async def search_papers(args):
    service = ServiceFactory.create_service()
    params = SearchParameters(
        query=args.query,
        max_results=args.max_results,
        date_from=args.date_from,
        date_to=args.date_to,
        categories=args.categories,
        batch_size=args.batch_size,
    )

    try:
        result = await service.search_papers(params)
        print(result.text)
    except Exception as e:
        print(f"Error searching papers: {str(e)}", file=sys.stderr)
        sys.exit(1)


async def analyze_paper(args):
    service = ServiceFactory.create_service()
    try:
        result = await service.analyze_paper(args.paper_id)
        print(result.text)
    except Exception as e:
        print(f"Error analyzing paper: {str(e)}", file=sys.stderr)
        sys.exit(1)


async def main_async():
    args = parse_args()

    if args.command == "search":
        await search_papers(args)
    elif args.command == "analyze":
        await analyze_paper(args)
    else:
        print("Please specify a command: search or analyze", file=sys.stderr)
        sys.exit(1)


def main():
    asyncio.run(main_async())
