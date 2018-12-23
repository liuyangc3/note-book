# Begin with TypeScript
https://github.com/Microsoft/TypeScript-React-Starter#typescript-react-starter
## Create new project
We'll create a new project called app:
```
yarn global add create-react-app
create-react-app app --scripts-version=react-scripts-ts
```
## Writing tests with Jest
install development dependency.
```
yarn add -D enzyme @types/enzyme enzyme-adapter-react-16 @types/enzyme-adapter-react-16 react-test-renderer
```
create a file called `src/setupTests.ts` that is automatically loaded when running tests:
```
import * as enzyme from 'enzyme';
import * as Adapter from 'enzyme-adapter-react-16';

enzyme.configure({ adapter: new Adapter() });
```
