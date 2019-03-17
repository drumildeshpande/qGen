import json;
import sys;

class Question:
	def __init__(self, questionId, difficulty, marks):
		self.id = questionId;
		self.difficulty = difficulty;
		self.marks = marks;

class QuestionPaperBuilder:
	def __init__(self):
		self.allQuestions = {};

	def addQuestion(self, question):
		if(question.difficulty not in self.allQuestions):
			self.allQuestions[question.difficulty] = {};
		self.allQuestions[question.difficulty][question.id] = question;

	def buildPaper(self, totalMarks, difficultyMarks):
		paperQuestions = [];
		validPaper = True;
		for d in difficultyMarks.keys():
			sectionMarks = (totalMarks*difficultyMarks[d]/100);
			questions = self.getMarksForDifficulty(d, sectionMarks);
			if(sectionMarks>0 and len(questions)==0):
				print "Question paper cannot be made";
				validPaper = False;
			else:
				paperQuestions.extend(questions);
		if(validPaper):
			print paperQuestions;

	def getMarksForDifficulty(self, difficulty, difficultyMarks):
		questions = [];
		self.getQuestions(difficultyMarks, self.allQuestions[difficulty].values(), len(self.allQuestions[difficulty]), questions);
		return questions;

	def getQuestions(self, K, wt, n, q):
		if(n==0 or K==0):
			if(K==0):
				return True;
			return False;
		if(wt[n-1].marks > K):
			return self.getQuestions(K, wt, n-1, q);
		else:
			lhs = self.getQuestions(K-wt[n-1].marks, wt, n-1, q);
			rhs = False;
			if(not lhs):
				rhs = self.getQuestions(K, wt, n-1, q);
			if(lhs):
				q.append(wt[n-1].id);
			return lhs or rhs; 


def main():
	with open(sys.argv[1]) as f:
		data = json.load(f);	

	qpBuilder = QuestionPaperBuilder();
	for q in data.get("totalQuestions"):
		qpBuilder.addQuestion(Question(q.get("questionId"), q.get("difficulty"), q.get("marks")));

	qpBuilder.buildPaper(data.get("questionPaperMarks").get("total"), data.get("questionPaperMarks").get("marksDistribution"));


if __name__ == '__main__':
	main();