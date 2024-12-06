//
// Copyright 2016 The BigDL Authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//

#pragma once

#include <string>
#include <vector>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <memory>
#include <vector>

#include "common.h"

using namespace std;

#ifdef __linux__
#define EXPORT_API extern "C"
#else
#define EXPORT_API extern "C" __declspec(dllexport)
#endif


class NPUModel;

#ifdef __cplusplus
extern "C" {
#endif
    EXPORT_API void load_tokenizer(tokenizer_params &tok_params, std::string model_str);

    EXPORT_API vector<int32_t> llm_tokenize(std::string prompt, bool add_special);

    EXPORT_API std::string llm_decode(vector<int32_t> tokens);

    EXPORT_API void* load_model_from_file(const char* model_path);

    EXPORT_API void load_config_from_file(npu_model_params &model_params, const char* model_path);

    EXPORT_API std::string add_chat_template(npu_model_params model_params, std::string input_prompt);

    EXPORT_API float* run_prefill(void* void_model, int32_t* embd_inp_ptr, int32_t embd_inp_size);

    EXPORT_API float* run_decode(void* void_model, int32_t input_token);

    EXPORT_API void run_prefill_with_logits(void* void_model, int32_t* embd_inp_ptr, int32_t embd_inp_size, float* logits, int32_t vocab_size);

    EXPORT_API void run_decode_with_logits(void* void_model, int32_t input_token, float* logits, int32_t vocab_size);

    EXPORT_API int32_t llm_sample_token(float* logits, bool greedy_search, int32_t vocab_size);

    EXPORT_API void reset(void* void_model);

#ifdef __cplusplus
}
#endif
