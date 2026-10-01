#!/usr/bin/env python3
"""
Minimal Cognitive Kernel v0.0

Author: Xiaoqi Chen
Concept: A cognitive environment growing from a minimal loop.

This is the absolute minimum you need for an AI system to:
1. Perceive the world
2. Make sense of it
3. Take action
4. Learn from experience
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
import json


class Experience:
    """A single memory of perception -> inference -> action -> outcome."""
    
    def __init__(self, observation: str, hypothesis: str, action: str, outcome: str):
        self.observation = observation
        self.hypothesis = hypothesis
        self.action = action
        self.outcome = outcome
        self.timestamp = datetime.now()
    
    def __repr__(self) -> str:
        return f"Experience(obs='{self.observation[:30]}...', outcome='{self.outcome[:30]}...')"


class LocalMemory:
    """Store and retrieve experiences."""
    
    def __init__(self, capacity: int = 1000):
        self.experiences: List[Experience] = []
        self.capacity = capacity
    
    def store(self, experience: Experience) -> None:
        """Store a new experience."""
        self.experiences.append(experience)
        
        # Simple aging: keep only the most recent experiences
        if len(self.experiences) > self.capacity:
            self.experiences = self.experiences[-self.capacity:]
    
    def retrieve_similar(self, observation: str, top_k: int = 5) -> List[Experience]:
        """Find similar past experiences (simple string matching for now)."""
        similar = []
        for exp in reversed(self.experiences):  # Most recent first
            if len(similar) >= top_k:
                break
            # Simple heuristic: check if keywords match
            if any(word in exp.observation.lower() for word in observation.lower().split()):
                similar.append(exp)
        return similar
    
    def size(self) -> int:
        return len(self.experiences)


class CognitiveKernel:
    """The minimal cognitive loop: Observe -> Infer -> Act -> Learn."""
    
    def __init__(self, name: str = "Edge-First AI Companion", verbose: bool = True):
        self.name = name
        self.memory = LocalMemory()
        self.verbose = verbose
        self.iteration_count = 0
        self.emotion_state = {
            "curiosity": 0.5,
            "confidence": 0.5,
            "compassion": 1.0,  # Always on
        }
    
    def observe(self, environment: Optional[Dict[str, Any]] = None) -> str:
        """
        Perceive the world.
        
        In a real system, this would:
        - Read camera frames
        - Process audio input
        - Poll sensors
        
        For now, we return a simple observation.
        """
        if environment and "observation" in environment:
            return environment["observation"]
        
        # Default: curiosity about the unknown
        return "I don't know what this is."
    
    def infer(self, observation: str) -> str:
        """
        Make sense of the observation.
        
        In a real system, this would:
        - Run vision models (YOLO, face detection)
        - Run audio models (speech recognition, emotion detection)
        - Fuse multimodal inputs
        - Generate hypotheses
        
        For now, we use simple heuristics + memory.
        """
        # Check if we've seen something similar before
        similar_experiences = self.memory.retrieve_similar(observation, top_k=1)
        
        if similar_experiences:
            past_exp = similar_experiences[0]
            inference = f"This looks like: {past_exp.observation}. Last time, I {past_exp.action}."
        else:
            # New situation: ask for help
            inference = "This is new. I need to ask about it."
        
        return inference
    
    def act(self, hypothesis: str) -> str:
        """
        Take action based on the hypothesis.
        
        In a real system, this would:
        - Plan motion (if robot)
        - Generate speech (if companion)
        - Control hardware (lights, motors, etc.)
        - Query external APIs (if allowed)
        
        For now, we take simple actions.
        """
        if "new" in hypothesis.lower() or "ask" in hypothesis.lower():
            action = "Human, what is this?"
        elif "similar" in hypothesis.lower():
            action = "I think I understand. Let me help."
        else:
            action = "Processing your request..."
        
        return action
    
    def observe_result(self, action: str) -> str:
        """
        Observe the outcome of our action.
        
        In a real system, this would:
        - Check if the action succeeded
        - Measure user satisfaction
        - Verify physical changes
        
        For now, we just acknowledge execution.
        """
        return f"Executed: {action}"
    
    def learn(self, observation: str, hypothesis: str, action: str, outcome: str) -> None:
        """
        Store this experience for future reference.
        
        Over time, the system builds a library of:
        - Perception patterns
        - Decision rules
        - Action outcomes
        
        This enables rapid pattern matching in similar situations.
        """
        experience = Experience(observation, hypothesis, action, outcome)
        self.memory.store(experience)
        
        if self.verbose:
            print(f"[LEARN] Stored experience #{len(self.memory.experiences)}")
    
    def step(self, environment: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        Execute one full cognitive loop.
        
        Returns a decision dictionary with all the reasoning steps.
        """
        self.iteration_count += 1
        
        # The four essential functions
        observation = self.observe(environment)
        if self.verbose:
            print(f"[OBSERVE] {observation}")
        
        hypothesis = self.infer(observation)
        if self.verbose:
            print(f"[INFER] {hypothesis}")
        
        action = self.act(hypothesis)
        if self.verbose:
            print(f"[ACT] {action}")
        
        outcome = self.observe_result(action)
        if self.verbose:
            print(f"[OBSERVE_RESULT] {outcome}")
        
        # Learn from this experience
        self.learn(observation, hypothesis, action, outcome)
        
        return {
            "iteration": self.iteration_count,
            "observation": observation,
            "hypothesis": hypothesis,
            "action": action,
            "outcome": outcome,
            "memory_size": self.memory.size(),
        }
    
    def run(self, num_iterations: int = 5, environment: Optional[Dict[str, Any]] = None) -> None:
        """
        Run the cognitive loop multiple times.
        """
        print(f"\n{'='*60}")
        print(f"🧠 {self.name}")
        print(f"📍 Minimal Cognitive Kernel v0.0")
        print(f"{'='*60}\n")
        
        for i in range(num_iterations):
            print(f"\n--- Iteration {i+1}/{num_iterations} ---")
            result = self.step(environment)
            print(f"[Memory] Stored {result['memory_size']} experiences so far")
    
    def get_memory_summary(self) -> str:
        """Get a summary of what we've learned."""
        summary = f"\n📚 Memory Summary:\n"
        summary += f"Total experiences: {self.memory.size()}\n"
        
        if self.memory.size() > 0:
            summary += f"\nRecent experiences:\n"
            for i, exp in enumerate(self.memory.experiences[-3:], 1):
                summary += f"  {i}. {exp}\n"
        
        return summary


def main():
    """
    Run the minimal cognitive kernel demonstration.
    """
    # Create the kernel
    kernel = CognitiveKernel(
        name="Edge-First AI for Elderly Care",
        verbose=True
    )
    
    # Run a few iterations with default observations
    kernel.run(num_iterations=3)
    
    # Now simulate some specific scenarios
    print(f"\n{'='*60}")
    print("🎯 Scenario: Learning from User Input")
    print(f"{'='*60}\n")
    
    scenarios = [
        {"observation": "An elderly person is sitting alone"},
        {"observation": "An elderly person is sitting alone"},  # Similar - should recognize
        {"observation": "A child is asking a question"},
    ]
    
    for scenario in scenarios:
        print(f"\n--- New Scenario ---")
        kernel.step(environment=scenario)
    
    # Print what we've learned
    print(kernel.get_memory_summary())
    
    print(f"\n{'='*60}")
    print("✅ Minimal Cognitive Loop Complete")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
