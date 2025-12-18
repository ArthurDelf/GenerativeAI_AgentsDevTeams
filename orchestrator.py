"""
Orchestrateur - Coordonne tous les agents de l'équipe
"""

from typing import Dict, List, Optional
from langchain_groq import ChatGroq

from agents.product_owner import ProductOwnerAgent
from agents.developer import DeveloperAgent
from agents.qa_engineer import QAAgent
from agents.tech_lead import TechLeadAgent


class TeamOrchestrator:
    def __init__(self, llm: ChatGroq, pdf_context: Optional[str] = None):

        self.llm = llm
        self.pdf_context = pdf_context
        
        # Initialiser tous les agents
        self.po = ProductOwnerAgent(llm=llm, pdf_context=pdf_context)
        self.dev = DeveloperAgent(llm=llm)
        self.qa = QAAgent(llm=llm)
        self.tech_lead = TechLeadAgent(llm=llm)
        self.execution_trace = []
        self.current_iteration = 0
    
    def run(
        self,
        user_request: str,
        max_iterations: int = 2,
        auto_fix: bool = True
    ) -> Dict:
        self.execution_trace.append({
            "step": "START",
            "message": " Démarrage de l'équipe AI Dev Team"
        })
        
        
        self.execution_trace.append({
            "step": "PO_START",
            "agent": "Product Owner",
            "message": " Analyse de la demande utilisateur..."
        })
        
        po_result = self.po.analyze_request(user_request)
        user_stories = po_result["raw_response"]
        
        self.execution_trace.append({
            "step": "PO_COMPLETE",
            "agent": "Product Owner",
            "message": " User Stories créées",
            "result": po_result
        })
        
       
        for iteration in range(1, max_iterations + 1):
            self.current_iteration = iteration
            
            self.execution_trace.append({
                "step": "ITERATION_START",
                "iteration": iteration,
                "message": f" Itération {iteration}/{max_iterations}"
            })
            
            
            self.execution_trace.append({
                "step": "DEV_START",
                "agent": "Developer",
                "iteration": iteration,
                "message": " Génération du code..."
            })
            
            if iteration == 1:
                dev_result = self.dev.generate_code(user_stories, iteration=iteration)
            else:
                
                last_qa = self._get_last_qa_result()
                feedback = self.qa.generate_feedback(last_qa)
                dev_result = self.dev.fix_code(feedback)
            
            code = dev_result["code"]
            
            self.execution_trace.append({
                "step": "DEV_COMPLETE",
                "agent": "Developer",
                "iteration": iteration,
                "message": " Code généré",
                "result": dev_result
            })
            
            
            self.execution_trace.append({
                "step": "QA_START",
                "agent": "QA Engineer",
                "iteration": iteration,
                "message": " Revue de code et génération de tests..."
            })
            
            qa_result = self.qa.review_code(code, user_stories)
            tests = qa_result["tests"]
            
            self.execution_trace.append({
                "step": "QA_COMPLETE",
                "agent": "QA Engineer",
                "iteration": iteration,
                "message": f" Revue terminée : {len(qa_result['critical_bugs'])} bugs critiques",
                "result": qa_result
            })
            
            
            self.execution_trace.append({
                "step": "TL_START",
                "agent": "Tech Lead",
                "iteration": iteration,
                "message": " Revue finale et décision..."
            })
            
            tl_result = self.tech_lead.final_review(
                code=code,
                tests=tests,
                user_stories=user_stories,
                qa_report=qa_result,
                iteration=iteration
            )
            
            decision = tl_result["decision"]
            
            self.execution_trace.append({
                "step": "TL_COMPLETE",
                "agent": "Tech Lead",
                "iteration": iteration,
                "message": f" Décision : {decision['status']}",
                "result": tl_result
            })
            
            
            should_continue, reason = self.tech_lead.should_iterate(decision)
            
            if decision["status"] == "VALIDATED":
                # Code validé, on arrête
                self.execution_trace.append({
                    "step": "SUCCESS",
                    "message": f" Projet validé à l'itération {iteration}"
                })
                break
            
            elif not auto_fix:
                
                self.execution_trace.append({
                    "step": "MANUAL_REVIEW",
                    "message": "⏸ Correction manuelle nécessaire (auto_fix=False)"
                })
                break
            
            elif iteration >= max_iterations:
                # Max itérations atteint
                self.execution_trace.append({
                    "step": "MAX_ITERATIONS",
                    "message": f" Nombre maximum d'itérations atteint ({max_iterations})"
                })
                break
            
            else:
                
                self.execution_trace.append({
                    "step": "CONTINUE",
                    "message": f" Nouvelle itération nécessaire : {reason}"
                })
        
        
        final_result = self._build_final_result(
            po_result=po_result,
            dev_result=dev_result,
            qa_result=qa_result,
            tl_result=tl_result
        )
        
        self.execution_trace.append({
            "step": "END",
            "message": " Exécution terminée"
        })
        
        return final_result
    
    def _get_last_qa_result(self) -> Dict:
        """Récupère le dernier résultat du QA"""
        for entry in reversed(self.execution_trace):
            if entry.get("step") == "QA_COMPLETE":
                return entry["result"]
        return {}
    
    def _build_final_result(
        self,
        po_result: Dict,
        dev_result: Dict,
        qa_result: Dict,
        tl_result: Dict
    ) -> Dict:
        
        
        return {
            "success": tl_result["decision"]["status"] == "VALIDATED",
            "iterations": self.current_iteration,
            "specifications": {
                "user_stories": po_result["raw_response"],
                "analysis": po_result["analysis"],
                "thoughts": po_result["thoughts"]
            },
            "code": {
                "final_code": dev_result["code"],
                "reasoning": dev_result["reasoning"],
                "iterations": len(self.dev.code_iterations),
                "thoughts": dev_result["thoughts"]
            },
            "tests": {
                "test_code": qa_result["tests"],
                "bugs_found": {
                    "critical": qa_result["critical_bugs"],
                    "minor": qa_result["minor_bugs"]
                },
                "quality_score": qa_result.get("quality_score"),
                "thoughts": qa_result["thoughts"]
            },
            "validation": {
                "status": tl_result["decision"]["status"],
                "justification": tl_result["decision"]["justification"],
                "actions": tl_result["decision"]["actions"],
                "thoughts": tl_result["thoughts"]
            },
            "execution_trace": self.execution_trace,
            "agents": {
                "po": self.po.get_trace(),
                "dev": self.dev.get_trace(),
                "qa": self.qa.get_trace(),
                "tech_lead": self.tech_lead.get_trace()
            }
        }
    
    def get_execution_summary(self) -> str:
        
        lines = ["# RÉSUMÉ DE L'EXÉCUTION", ""]
        
        for entry in self.execution_trace:
            step = entry.get("step", "")
            agent = entry.get("agent", "")
            iteration = entry.get("iteration", "")
            message = entry.get("message", "")
            
            if agent:
                line = f"**[{agent}]** "
            else:
                line = ""
            
            if iteration:
                line += f"(Itération {iteration}) "
            
            line += message
            lines.append(line)
        
        return "\n".join(lines)



