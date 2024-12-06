# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0


def pytest_addoption(parser):
    parser.addoption("--storage_root", action="store", default=None)
    parser.addoption("--test_remote", action="store_true", default=False)
    parser.addoption("--api_endpoint", action="store", default=None)
    parser.addoption("--api_token", action="store", default=None)
    parser.addoption("--api_insecure", action="store_true", default=False)
    parser.addoption("--skip_workflows", action="store_true", default=False)
    parser.addoption("--skip_analyses", action="store_true", default=False)
    parser.addoption("--skip_documentation", action="store_true", default=False)
    parser.addoption("--skip_huggingface", action="store_true", default=False)
    parser.addoption("--skip_errors", action="store_true", default=False)
    parser.addoption("--enable_vllm", action="store_true", default=False)
    parser.addoption("--enable_comparisons", action="store_true", default=False)
