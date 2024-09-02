from experimenter import Experimenter
from expo.MCTS import create_initial_state
from expo.dataset import generate_task_requirement
from expo.utils import mcts_logger, load_execute_notebook, get_exp_pool_path
from exp_optimizer.expo.insights.instruction_generator import InstructionGenerator
from expo.research_assistant import ResearchAssistant

EXPS_PROMPT = """
When doing the tasks, you can refer to the insights below:
{experience}

"""




class AugExperimenter(Experimenter):
    result_path : str = "results/aug"

    async def run_experiment(self):
        state = create_initial_state(self.args.task, start_task_id=1, data_config=self.data_config, low_is_better=self.args.low_is_better, name="")
        user_requirement = state["requirement"]
        exp_pool_path = get_exp_pool_path(self.args.task, self.data_config, pool_name="ds_analysis_pool")
        exp_pool = InstructionGenerator.load_analysis_pool(exp_pool_path)
        if self.args.aug_mode == "single":
            exps = InstructionGenerator._random_sample(exp_pool, self.args.num_experiments)
            exps = [exp["Analysis"] for exp in exps]
        elif self.args.aug_mode == "set":
            exp_set = InstructionGenerator.sample_instruction_set(exp_pool)
            exp_set_text = "\n".join([f"{exp['task_id']}: {exp['Analysis']}" for exp in exp_set])
            exps = [exp_set_text] * self.args.num_experiments
        else:
            raise ValueError(f"Invalid mode: {self.args.aug_mode}")
        
        results = []
        for i in range(self.args.num_experiments):
            di = ResearchAssistant(node_id=str(i), use_reflection=self.args.use_reflection)
            di.role_dir = f"{di.role_dir}_{self.args.task}"
            requirement = user_requirement + EXPS_PROMPT.format(experience=exps[i])
            print(requirement)
            await di.run(requirement)
            score_dict = await di.get_score(low_is_better=False)
            score_dict = self.evaluate(score_dict, state)
            results.append({
                "idx": i,
                "score_dict": score_dict,
                "aug_mode": self.args.aug_mode,
                "insights" : exps[i],
                "user_requirement": user_requirement,
                "args": self.args
            })
        scores = [score_dict["test_score"] for score_dict in scores]
        avg_score = sum(scores) / len(scores)
        best_score = max(scores) if not self.args.low_is_better else min(scores)
        best_score_idx = scores.index(best_score)
        results.insert(0, {"avg_score": avg_score, "best_score": best_score, "best_score_idx": best_score_idx})
        self.save_results(results)

        
        